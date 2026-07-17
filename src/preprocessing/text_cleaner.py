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