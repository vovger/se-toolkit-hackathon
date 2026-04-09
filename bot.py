import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import database as db

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I'm a contact manager bot.\n\n"
        "Commands:\n"
        "/addfield <name> - create a new field (e.g., birthday)\n"
        "/fields - show all fields"
    )

async def addfield(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /addfield <field_name>")
        return
    
    field_name = " ".join(context.args).lower()
    success = db.add_field(field_name)
    
    if success:
        await update.message.reply_text(f"✅ Field '{field_name}' created!")
    else:
        await update.message.reply_text(f"⚠️ Field '{field_name}' already exists.")

async def fields(update: Update, context: ContextTypes.DEFAULT_TYPE):
    all_fields = db.get_all_fields()
    if not all_fields:
        await update.message.reply_text("📭 No fields yet. Create one with /addfield")
    else:
        fields_list = "\n".join(f"• {f}" for f in all_fields)
        await update.message.reply_text(f"📋 Existing fields:\n{fields_list}")

def main():
    db.init_db()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addfield", addfield))
    app.add_handler(CommandHandler("fields", fields))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
