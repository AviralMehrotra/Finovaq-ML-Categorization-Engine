import re

BANKING_STOP_WORDS = {
    "upi", "ybl", "okhdfc", "neft", "imps", "ach", "pos", "razorpay", 
    "auto", "india", "blr", "hyd", "mum", "delhi", "xyz", "001", "123", "123456",
    "paytm", "yesb0ptm", "yesb0ptmupi", "pay", "payment", "sent", "using", "from",
    "phone", "digital", "goog", "payments", "axisbank", "utib", "ibl", "icic",
    "punb", "sbi", "sbin", "hdfc", "hdfcbank", "rupi", "erupi", "intent", "upiintent",
    "rtgs", "fund", "transfer", "tpt", "mob", "net", "banking", "chrg", "charge",
    "sms", "alert", "chg", "fee", "gst", "tx", "txn", "ref", "no", "cr", "dr",
    "payu", "razor", "easebuzz", "kotak", "kotakpay", "merchant", "retail", "limited",
    "pvt", "ltd", "corporation", "corp", "inc"
}

# Honorifics that strongly signal a personal name follows
_HONORIFICS = re.compile(
    r'\b(mr|mrs|ms|dr|shri|smt|prof|er)\b',
    re.IGNORECASE
)

# Words that strongly indicate this is a company/business, not a personal name
BUSINESS_KEYWORDS = {
    "DIGITAL", "LIMITED", "LTD", "PAY", "GROCERIES", "BOOK", "POINT", "MARKETPLACE",
    "RETAIL", "SERVICES", "STORE", "STORES", "TECH", "MEDIA", "ENTERTAINMENT", "TRAVELS",
    "TRAVEL", "FOOD", "CAFE", "RESTAURANT", "CLOTHING", "FASHION", "INDIA", "NIPPON",
    "MUTUAL", "FUND", "MF", "INSURANCE", "BANK", "COMMUNICATIONS", "AGENCY", "LABS",
    "SOLUTIONS", "VENTURES", "ENTERPRISES", "SYSTEMS", "GLOBAL", "CORP", "ASSOCIATES",
    "PARTNERS", "ACADEMY", "UNIVERSITY", "SCHOOL", "COLLEGE", "CLINIC", "HOSPITAL",
    "PHARMACY", "MEDICINES", "SUPERMARKET", "MART", "AGRO", "DESIGNS", "AUTOMOTIVE",
    "MOTORS", "CABS", "PETROLEUM", "FUELS", "POWER", "GAS", "ELECTRIC", "ONLINE",
    "SHOP", "SHOPS", "PAYMENTS", "BILL", "RECHARGE", "TELECOM", "MOBILE", "INTERNET",
    "BROADBAND", "FIBER"
}

def is_personal_transfer(description: str) -> bool:
    """Return True if the transaction description looks like a P2P transfer to a person."""
    text = description.upper()

    # Quick wins: common honorifics in the string
    if _HONORIFICS.search(description):
        return True

    # Try to extract the merchant segment (text between first UPI- and the @ or next dash)
    # We match UPI- or NEFT- or IMPS- then capture everything up to the next '-' or '@'
    match = re.search(
        r'(?:UPI|IMPS|NEFT)[-/]([A-Z][A-Z0-9 _\.]+?)(?:[-@]|$)',
        text
    )
    if match:
        candidate = match.group(1).strip()
        words = candidate.split()
        
        # Personal names are typically 2-4 words, all alpha, no digit
        if 2 <= len(words) <= 4 and all(w.isalpha() for w in words):
            # Check if any of the words are known business keywords
            if not any(w in BUSINESS_KEYWORDS for w in words):
                return True

    return False

def lowercase_text(text):
    return text.lower()

def remove_vpas(text):
    # Remove VPAs (e.g. @okicici, @ptybl, @okhdfc, etc.)
    return re.sub(r'@[a-zA-Z0-9.-]+', ' ', text)

def remove_long_numeric(text):
    # Remove long numeric strings (e.g. transaction IDs usually 6+ digits)
    return re.sub(r'\b\d{6,}\b', ' ', text)

def remove_special_characters(text):
    return re.sub(r"[^a-zA-Z0-9\s]", " ", text)

def remove_extra_spaces(text):
    return " ".join(text.split())

def remove_banking_words(text):
    words = text.split()

    words = [
        word
        for word in words
        if word not in BANKING_STOP_WORDS and not word.isdigit() and len(word) > 1
    ]

    return " ".join(words)

def clean_text(text):
    text = lowercase_text(text)
    text = remove_vpas(text)
    text = remove_long_numeric(text)
    text = remove_special_characters(text)
    text = remove_banking_words(text)
    text = remove_extra_spaces(text)

    return text