"""
Localization module for LIQ Invoice.
Supported languages: English (en), Russian (ru), Ukrainian (uk)
"""

LANGUAGES = {
    "en": "English",
    "ru": "Русский",
    "uk": "Українська",
}

TRANSLATIONS = {
    "en": {
             
        "app_title": "LIQ Invoice",
        "app_brand": "⚡ LIQ Invoice",

                 
        "your_company": "Your company",
        "company_name": "Company name",
        "address_tax_id": "Address / Tax ID",
        "email": "Email",
        "phone": "Phone",
        "upload_logo": "Upload logo",
        "settings": "Settings",
        "currency": "Currency",
        "tax_rate": "Tax %",
        "accent_color": "Accent color",
        "save_company_data": "Save company data",

                 
        "new_invoice": "New Invoice",
        "preview": "Preview",
        "create_pdf": "Create PDF",

                        
        "recipient_client": "RECIPIENT (CLIENT)",
        "client_company_name": "Client company name / full name",
        "client_email": "Client email",
        "client_address": "Client address",
        "client_tax_id": "Client tax ID",

                      
        "invoice_details": "INVOICE DETAILS",
        "invoice_number": "Invoice number",
        "issue_date": "Issue date",
        "due_date": "Due date",
        "project_order": "Project / order",

               
        "invoice_items": "INVOICE ITEMS",
        "col_no": "#",
        "col_description": "Description",
        "col_qty": "Qty",
        "col_price": "Price",
        "col_amount": "Amount",
        "item_desc_placeholder": "Service / item description",
        "item_qty_placeholder": "Qty",
        "item_price_placeholder": "Price",
        "add_item": "Add item",

                
        "subtotal": "Subtotal:",
        "tax_label": "Tax ({rate}%):",
        "total_due": "Total due:",

               
        "notes_requisites": "NOTES / PAYMENT DETAILS",
        "notes_default": "Bank details:\nIBAN: UA...",

                 
        "warning": "Warning",
        "no_items_warning": "Add at least one item with a description.",
        "no_client_warning": "No client",
        "no_client_msg": "Please enter the client's name.",
        "at_least_one_item": "There must be at least one item.",
        "saved": "Saved",
        "saved_msg": "✓ Company data saved.\nIt will load automatically next time.",
        "done": "✓ Done",
        "done_msg": "PDF saved:\n{path}\n\nInvoice #{num} for {currency}{amount}",
        "error": "Error",
        "error_pdf_msg": "Could not create PDF:\n{err}",
        "select_logo": "Select logo",
        "images": "Images",
        "select_accent_color": "Select accent color",
        "save_invoice_as": "Save invoice as",
        "pdf_file": "PDF file",

                        
        "preview_title": "Preview — Invoice #{num}",
        "preview_heading": "PDF Preview",
        "preview_sub": "The invoice will look exactly like this when saved.",
        "preview_unavailable": "📄 PDF created successfully.\nPreview is not available in this environment.\nClick “Create PDF” to save the file.",
        "close": "Close",
        "generating_preview": "Generating preview…",

                     
        "pdf_invoice_word": "INVOICE",
        "pdf_date": "Date:",
        "pdf_due": "Due date:",
        "pdf_project": "Project:",
        "pdf_from": "FROM:",
        "pdf_to": "TO:",
        "pdf_no": "#",
        "pdf_description": "Description",
        "pdf_qty": "Qty",
        "pdf_price": "Price, {cur}",
        "pdf_amount": "Amount, {cur}",
        "pdf_subtotal": "Subtotal:",
        "pdf_tax": "Tax ({rate}%):",
        "pdf_total": "Total due:",
        "pdf_notes_title": "Payment details & notes",
        "pdf_footer": "Created with LIQ Invoice",

                                           
        "preferences": "Preferences",
        "appearance": "Appearance",
        "theme": "Theme",
        "theme_light": "Light",
        "theme_dark": "Dark",
        "theme_system": "System",
        "language": "Language",
        "more_settings_soon": "More options coming soon",

                     
        "tab_new_invoice": "New Invoice",
        "tab_history": "History",
        "history_title": "Invoice History",
        "history_empty": "No invoices yet.\nInvoices you create will appear here automatically.",
        "history_col_date": "Date",
        "history_col_number": "Invoice #",
        "history_col_client": "Client",
        "history_col_amount": "Amount",
        "history_col_status": "Status",
        "status_unpaid": "Unpaid",
        "status_paid": "Paid",
        "status_cancelled": "Cancelled",
        "open_pdf": "Open PDF",
        "file_missing": "File not found",
        "file_missing_msg": "This invoice's PDF file could no longer be found on disk:\n{path}",
        "delete_entry": "Delete",
        "delete_entry_confirm_title": "Delete from history",
        "delete_entry_confirm_msg": "Remove invoice #{num} from history?\nThis won't delete the PDF file itself.",
        "history_search_placeholder": "Search by client or invoice #",
    },

    "ru": {
        "app_title": "LIQ Invoice",
        "app_brand": "⚡ LIQ Invoice",

        "your_company": "Ваша компания",
        "company_name": "Название компании",
        "address_tax_id": "Адрес / ИНН",
        "email": "Email",
        "phone": "Телефон",
        "upload_logo": "Загрузить логотип",
        "settings": "Настройки",
        "currency": "Валюта",
        "tax_rate": "НДС %",
        "accent_color": "Цвет акцента",
        "save_company_data": "Сохранить данные компании",

        "new_invoice": "Новый счёт",
        "preview": "Предпросмотр",
        "create_pdf": "Создать PDF",

        "recipient_client": "ПОЛУЧАТЕЛЬ (КЛИЕНТ)",
        "client_company_name": "Название компании / ФИО клиента",
        "client_email": "Email клиента",
        "client_address": "Адрес клиента",
        "client_tax_id": "ИНН / ЕГРПОУ клиента",

        "invoice_details": "ДЕТАЛИ СЧЁТА",
        "invoice_number": "Номер счёта",
        "issue_date": "Дата выставления",
        "due_date": "Срок оплаты",
        "project_order": "Проект / заказ",

        "invoice_items": "ПОЗИЦИИ СЧЁТА",
        "col_no": "№",
        "col_description": "Описание",
        "col_qty": "Кол-во",
        "col_price": "Цена",
        "col_amount": "Сумма",
        "item_desc_placeholder": "Описание услуги / товара",
        "item_qty_placeholder": "Кол-во",
        "item_price_placeholder": "Цена",
        "add_item": "Добавить позицию",

        "subtotal": "Подытог:",
        "tax_label": "НДС ({rate}%):",
        "total_due": "Итого к оплате:",

        "notes_requisites": "КОММЕНТАРИЙ / РЕКВИЗИТЫ",
        "notes_default": "Банковские реквизиты:\nСчёт: UA...",

        "warning": "Внимание",
        "no_items_warning": "Добавьте хотя бы одну позицию с описанием.",
        "no_client_warning": "Нет клиента",
        "no_client_msg": "Укажите название клиента.",
        "at_least_one_item": "Должна быть хотя бы одна позиция.",
        "saved": "Сохранено",
        "saved_msg": "✓ Данные компании сохранены.\nПри следующем запуске они подгрузятся автоматически.",
        "done": "✓ Готово",
        "done_msg": "PDF сохранён:\n{path}\n\nСчёт №{num} на сумму {currency}{amount}",
        "error": "Ошибка",
        "error_pdf_msg": "Не удалось создать PDF:\n{err}",
        "select_logo": "Выберите логотип",
        "images": "Изображения",
        "select_accent_color": "Выберите цвет акцента",
        "save_invoice_as": "Сохранить счёт как",
        "pdf_file": "PDF файл",

        "preview_title": "Предпросмотр — Счёт №{num}",
        "preview_heading": "Предпросмотр PDF",
        "preview_sub": "Счёт будет выглядеть именно так при сохранении.",
        "preview_unavailable": "📄 PDF создан успешно.\nПредпросмотр недоступен в этой среде.\nНажмите «Создать PDF», чтобы сохранить файл.",
        "close": "Закрыть",
        "generating_preview": "Формирование предпросмотра…",

        "pdf_invoice_word": "СЧЁТ",
        "pdf_date": "Дата:",
        "pdf_due": "Оплатить до:",
        "pdf_project": "Проект:",
        "pdf_from": "ОТ:",
        "pdf_to": "КОМУ:",
        "pdf_no": "№",
        "pdf_description": "Описание",
        "pdf_qty": "Кол-во",
        "pdf_price": "Цена, {cur}",
        "pdf_amount": "Сумма, {cur}",
        "pdf_subtotal": "Подытог:",
        "pdf_tax": "НДС ({rate}%):",
        "pdf_total": "Итого к оплате:",
        "pdf_notes_title": "Реквизиты и комментарий",
        "pdf_footer": "Создано с помощью LIQ Invoice",

        "preferences": "Настройки",
        "appearance": "Внешний вид",
        "theme": "Тема",
        "theme_light": "Светлая",
        "theme_dark": "Тёмная",
        "theme_system": "Системная",
        "language": "Язык",
        "more_settings_soon": "Больше настроек скоро появится",

                     
        "tab_new_invoice": "Новый счёт",
        "tab_history": "История",
        "history_title": "История счетов",
        "history_empty": "Пока нет счетов.\nСозданные счета будут появляться здесь автоматически.",
        "history_col_date": "Дата",
        "history_col_number": "№ счёта",
        "history_col_client": "Клиент",
        "history_col_amount": "Сумма",
        "history_col_status": "Статус",
        "status_unpaid": "Не оплачен",
        "status_paid": "Оплачен",
        "status_cancelled": "Отменён",
        "open_pdf": "Открыть PDF",
        "file_missing": "Файл не найден",
        "file_missing_msg": "PDF этого счёта больше не найден на диске:\n{path}",
        "delete_entry": "Удалить",
        "delete_entry_confirm_title": "Удалить из истории",
        "delete_entry_confirm_msg": "Удалить счёт №{num} из истории?\nСам PDF-файл при этом не удаляется.",
        "history_search_placeholder": "Поиск по клиенту или номеру счёта",
    },

    "uk": {
        "app_title": "LIQ Invoice",
        "app_brand": "⚡ LIQ Invoice",

        "your_company": "Ваша компанія",
        "company_name": "Назва компанії",
        "address_tax_id": "Адреса / ІПН",
        "email": "Email",
        "phone": "Телефон",
        "upload_logo": "Завантажити логотип",
        "settings": "Налаштування",
        "currency": "Валюта",
        "tax_rate": "ПДВ %",
        "accent_color": "Колір акценту",
        "save_company_data": "Зберегти дані компанії",

        "new_invoice": "Новий рахунок",
        "preview": "Попередній перегляд",
        "create_pdf": "Створити PDF",

        "recipient_client": "ОТРИМУВАЧ (КЛІЄНТ)",
        "client_company_name": "Назва компанії / ПІБ клієнта",
        "client_email": "Email клієнта",
        "client_address": "Адреса клієнта",
        "client_tax_id": "ІПН / ЄДРПОУ клієнта",

        "invoice_details": "ДЕТАЛІ РАХУНКА",
        "invoice_number": "Номер рахунка",
        "issue_date": "Дата виставлення",
        "due_date": "Термін оплати",
        "project_order": "Проєкт / замовлення",

        "invoice_items": "ПОЗИЦІЇ РАХУНКА",
        "col_no": "№",
        "col_description": "Опис",
        "col_qty": "Кіл-сть",
        "col_price": "Ціна",
        "col_amount": "Сума",
        "item_desc_placeholder": "Опис послуги / товару",
        "item_qty_placeholder": "Кіл-сть",
        "item_price_placeholder": "Ціна",
        "add_item": "Додати позицію",

        "subtotal": "Підсумок:",
        "tax_label": "ПДВ ({rate}%):",
        "total_due": "Разом до сплати:",

        "notes_requisites": "КОМЕНТАР / РЕКВІЗИТИ",
        "notes_default": "Банківські реквізити:\nРахунок: UA...",

        "warning": "Увага",
        "no_items_warning": "Додайте хоча б одну позицію з описом.",
        "no_client_warning": "Немає клієнта",
        "no_client_msg": "Вкажіть назву клієнта.",
        "at_least_one_item": "Має бути хоча б одна позиція.",
        "saved": "Збережено",
        "saved_msg": "✓ Дані компанії збережено.\nПри наступному запуску вони підвантажаться автоматично.",
        "done": "✓ Готово",
        "done_msg": "PDF збережено:\n{path}\n\nРахунок №{num} на суму {currency}{amount}",
        "error": "Помилка",
        "error_pdf_msg": "Не вдалося створити PDF:\n{err}",
        "select_logo": "Виберіть логотип",
        "images": "Зображення",
        "select_accent_color": "Виберіть колір акценту",
        "save_invoice_as": "Зберегти рахунок як",
        "pdf_file": "PDF файл",

        "preview_title": "Попередній перегляд — Рахунок №{num}",
        "preview_heading": "Попередній перегляд PDF",
        "preview_sub": "Рахунок виглядатиме саме так після збереження.",
        "preview_unavailable": "📄 PDF створено успішно.\nПопередній перегляд недоступний у цьому середовищі.\nНатисніть «Створити PDF», щоб зберегти файл.",
        "close": "Закрити",
        "generating_preview": "Формування перегляду…",

        "pdf_invoice_word": "РАХУНОК",
        "pdf_date": "Дата:",
        "pdf_due": "Оплатити до:",
        "pdf_project": "Проєкт:",
        "pdf_from": "ВІД:",
        "pdf_to": "КОМУ:",
        "pdf_no": "№",
        "pdf_description": "Опис",
        "pdf_qty": "Кіл-сть",
        "pdf_price": "Ціна, {cur}",
        "pdf_amount": "Сума, {cur}",
        "pdf_subtotal": "Підсумок:",
        "pdf_tax": "ПДВ ({rate}%):",
        "pdf_total": "Разом до сплати:",
        "pdf_notes_title": "Реквізити та коментар",
        "pdf_footer": "Створено за допомогою LIQ Invoice",

        "preferences": "Налаштування",
        "appearance": "Зовнішній вигляд",
        "theme": "Тема",
        "theme_light": "Світла",
        "theme_dark": "Темна",
        "theme_system": "Системна",
        "language": "Мова",
        "more_settings_soon": "Незабаром тут з'являться інші опції",

                     
        "tab_new_invoice": "Новий рахунок",
        "tab_history": "Історія",
        "history_title": "Історія рахунків",
        "history_empty": "Поки немає рахунків.\nСтворені рахунки з'являтимуться тут автоматично.",
        "history_col_date": "Дата",
        "history_col_number": "№ рахунка",
        "history_col_client": "Клієнт",
        "history_col_amount": "Сума",
        "history_col_status": "Статус",
        "status_unpaid": "Не оплачено",
        "status_paid": "Оплачено",
        "status_cancelled": "Скасовано",
        "open_pdf": "Відкрити PDF",
        "file_missing": "Файл не знайдено",
        "file_missing_msg": "PDF цього рахунка більше не знайдено на диску:\n{path}",
        "delete_entry": "Видалити",
        "delete_entry_confirm_title": "Видалити з історії",
        "delete_entry_confirm_msg": "Видалити рахунок №{num} з історії?\nСам PDF-файл при цьому не видаляється.",
        "history_search_placeholder": "Пошук за клієнтом або номером рахунка",
    },
}


class I18n:
    """Simple translation helper with a mutable current-language pointer."""

    def __init__(self, lang="en"):
        self.lang = lang if lang in TRANSLATIONS else "en"
        self.listeners = []

    def set_lang(self, lang):
        if lang in TRANSLATIONS:
            self.lang = lang
            for cb in self.listeners:
                cb()

    def on_change(self, callback):
        self.listeners.append(callback)

    def t(self, key, **kwargs):
        text = TRANSLATIONS.get(self.lang, TRANSLATIONS["en"]).get(key)
        if text is None:
            text = TRANSLATIONS["en"].get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text