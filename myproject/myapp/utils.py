import libscrc

def generate_promptpay_payload(mobile: str, amount: float) -> str:
    def _format_tlv(tag, value):
        return f"{tag}{len(value):02d}{value}"
    mobile = mobile.strip().replace("-", "")
    if mobile.startswith("0"):
        mobile = "66" + mobile[1:]
    merchant_info = _format_tlv("00", "A000000677010111") + _format_tlv("01", mobile)
    payload = (
        _format_tlv("00", "01") +
        _format_tlv("01", "11") +
        _format_tlv("29", merchant_info) +
        _format_tlv("53", "764") +
        _format_tlv("54", f"{amount:.2f}") +
        _format_tlv("58", "TH")
    )
    payload += "6304"
    crc = libscrc.ccitt_false(payload.encode('ascii')).to_bytes(2, 'big').hex().upper()
    return payload + crc