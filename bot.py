import os
import json
import io
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

import database as db

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello! I'm a contact manager bot.\n\n"
        "**Commands:**\n"
        "/addfield <name> - create a new field (e.g., birthday)\n"
        "/fields - show all fields\n"
        "/add <person> <field> <value> - add data about a person\n"
        "/find <person> - find all data about a person\n"
        "/findby <field> <value> - find people by field value\n"
        "/edit <person> <field> <new_value> - edit existing data\n"
        "/list - show all people\n"
        "/delete <person> - delete a person\n"
        "/export - export all contacts to JSON file",
        parse_mode="Markdown"
    )

async def addfield(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /addfield <field_name>\nExample: /addfield birthday")
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
        await update.message.reply_text(f"📋 **Existing fields:**\n{fields_list}", parse_mode="Markdown")

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
        await update.message.reply_text("❌ Usage: /find <person_name>\nExample: /find Anna")
        return
    
    person_name = " ".join(context.args)
    results = db.find_person(person_name)
    
    if not results:
        await update.message.reply_text(f"📭 No data found for '{person_name}'")
        return
    
    message = f"📇 **{person_name}**\n"
    for _, field_name, value in results:
        message += f"   • {field_name}: {value}\n"
    
    await update.message.reply_text(message, parse_mode="Markdown")

async def findby(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("❌ Usage: /findby <field> <value>\nExample: /findby birthday 15.05")
        return
    
    field_name = context.args[0].lower()
    value = " ".join(context.args[1:])
    
    results, error = db.find_by_value(field_name, value)
    
    if error:
        await update.message.reply_text(f"❌ {error}")
        return
    
    if not results:
        await update.message.reply_text(f"📭 No one found with {field_name} containing '{value}'")
        return
    
    message = f"🔍 Found {len(results)} person(s) with {field_name} containing '{value}':\n\n"
    for name, val in results:
        message += f"• **{name}**: {val}\n"
    
    await update.message.reply_text(message, parse_mode="Markdown")

async def edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text("❌ Usage: /edit <person_name> <field> <new_value>\nExample: /edit Anna phone +79998887766")
        return
    
    person_name = context.args[0]
    field_name = context.args[1].lower()
    new_value = " ".join(context.args[2:])
    
    success, message = db.edit_contact_data(person_name, field_name, new_value)
    
    if success:
        await update.message.reply_text(f"✅ {message}")
    else:
        await update.message.reply_text(f"❌ {message}")

async def list_people(update: Update, context: ContextTypes.DEFAULT_TYPE):
    people = db.get_all_people()
    
    if not people:
        await update.message.reply_text("📭 No people saved yet. Add someone with /add")
    else:
        people_list = "\n".join(f"• {p}" for p in people)
        await update.message.reply_text(f"📋 **Saved people ({len(people)}):**\n{people_list}", parse_mode="Markdown")

async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /delete <person_name>\nExample: /delete Anna")
        return
    
    person_name = " ".join(context.args)
    success, message = db.delete_person(person_name)
    
    if success:
        await update.message.reply_text(f"✅ {message}")
    else:
        await update.message.reply_text(f"❌ {message}")

async def export(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = db.export_all_data()
    
    if not data:
        await update.message.reply_text("📭 No contacts to export")
        return
    
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    
    file = io.BytesIO(json_str.encode('utf-8'))
    file.name = "contacts_export.json"
    
    await update.message.reply_document(
        document=file,
        caption=f"✅ Exported {len(data)} contact(s)"
    )

def main():
    db.init_db()
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addfield", addfield))
    app.add_handler(CommandHandler("fields", fields))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("find", find))
    app.add_handler(CommandHandler("findby", findby))
    app.add_handler(CommandHandler("edit", edit))
    app.add_handler(CommandHandler("list", list_people))
    app.add_handler(CommandHandler("delete", delete))
    app.add_handler(CommandHandler("export", export))
    
    print("🤖 Bot is running...")
    print("Commands available: start, addfield, fields, add, find, findby, edit, list, delete, export")
    app.run_polling()

if __name__ == "__main__":
    main()

