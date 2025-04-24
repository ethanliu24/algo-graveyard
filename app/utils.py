def sanitize_str(s: str):
  s = s.strip()
  return s[0].upper() + s[1:] if s else s
