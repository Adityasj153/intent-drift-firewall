from firewall.intent_extractor import IntentExtractor

extractor = IntentExtractor()

intent = extractor.extract("Calculate 50 + 70")

print(intent)