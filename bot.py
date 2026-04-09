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
        "/fields - show all fields\n"
        "/add <person> <field> <value> - add data about a person\n"
        "/find <person> - find all data about a person\n"
        "/list - show all people\n"
        "/delete <person> - delete a person"
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

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text("❌ Usage: /add <person_name> <field> <value>\nExample: /add Anna birthday 15.05")
        return
    
    person_name = context.args[0]
    field_name = context.args[1].lower()
    value = " ".join(context.args[2:])
    
    success, message = db.add_contact_data(person_name, field_name, value)
    
    if success:
        await update.message.reply_text(f"✅ {message}")
    else:
        await update.message.reply_text(f"❌ {message}")

async def find(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /find <person_name>")
        return
    
    person_name = " ".join(context.args)
    results = db.find_person(person_name)
    
    if not results:
        await update.message.reply_text(f"📭 No data found for '{person_name}'")
        return
    
    message = f"📇 **{person_name}**\n"
    for _, field_name, value in results:
        message += f"   • {field_name}: {value}\n"
    
    await update.message.reply_text(message)

async def list_people(update: Update, context: ContextTypes.DEFAULT_TYPE):
    people = db.get_all_people()
    
    if not people:
        await update.message.reply_text("📭 No people saved yet. Add someone with /add")
    else:
        people_list = "\n".join(f"• {p}" for p in people)
        await update.message.reply_text(f"📋 Saved people:\n{people_list}")

async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /delete <person_name>")
        return
    
    person_name = " ".join(context.args)
    success, message = db.delete_person(person_name)
    
    if success:
        await update.message.reply_text(f"✅ {message}")
    else:
        await update.message.reply_text(f"❌ {message}")

def main():
    db.init_db()
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addfield", addfield))
    app.add_handler(CommandHandler("fields", fields))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("find", find))
    app.add_handler(CommandHandler("list", list_people))
    app.add_handler(CommandHandler("delete", delete))
    
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
