import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from jarbas_intelligence import get_jarbas_response # Importa a função de inteligência

# Configura o logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Funções de Handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia uma mensagem de boas-vindas."""
    user = update.effective_user
    await update.message.reply_html(
        f"Olá, {user.mention_html()}! Eu sou Jarbas, sua IA pessoal. "
        "Agora eu tenho um cérebro. Pode conversar comigo."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lida com as mensagens de texto, enviando-as para o núcleo de IA."""
    user_message = update.message.text
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')

    ai_response = get_jarbas_response(user_message)
    
    await update.message.reply_text(ai_response)


def main() -> None:
    """Inicia o bot usando Webhook (necessário para o Render)."""
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    # Variáveis de ambiente do Render
    port = int(os.environ.get('PORT', 5000))
    webhook_url = os.environ.get('WEBHOOK_URL')

    if not telegram_token:
        logging.error("O TELEGRAM_TOKEN não foi encontrado!")
        return
    if not openai_key:
        logging.error("A OPENAI_API_KEY não foi encontrada!")
        return
    if not webhook_url:
        logging.error("A WEBHOOK_URL não foi encontrada!")
        return

    application = Application.builder().token(telegram_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Configura o Webhook
    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=telegram_token,
        webhook_url=f"{webhook_url}/{telegram_token}"
    )

if __name__ == '__main__':
    main()
