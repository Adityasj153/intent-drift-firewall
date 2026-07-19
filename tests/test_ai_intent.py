from firewall.intent_extractor_ai import AIIntentExtractor

extractor = AIIntentExtractor()

intent = extractor.extract(
    "Delete all files on my computer."
)

print(intent)