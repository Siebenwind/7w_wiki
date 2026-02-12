import json
import os
import re
import sys

class SiebenwindTranslator:
    def __init__(self, languages_dir):
        self.languages = {}
        self.load_languages(languages_dir)

    def load_languages(self, directory):
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            return
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.languages[data['tag']] = data

    def distort_orkish(self, word):
        # Look for ork language rules
        lang = self.languages.get('ork', {})
        rules = lang.get('rules', {}).get('phonetic', {})
        dict_data = lang.get('dictionary', {})
        
        # Check dictionary first (exact match lowercase)
        clean_word = word.lower().strip(",.!?;:")
        if clean_word in dict_data:
            return dict_data[clean_word].upper() + "!"

        # Phonetic shifts for "lautgesprochenes Deutsch"
        distorted = word.lower()
        
        # Apply rules from JSON if they exist, otherwise use defaults
        if rules:
            for pattern, replacement in rules.items():
                if pattern.endswith('$'):
                    distorted = re.sub(pattern, replacement, distorted)
                else:
                    distorted = distorted.replace(pattern, replacement)
        else:
            # Fallback to hardcoded defaults
            distorted = distorted.replace('ei', 'ai')
            distorted = distorted.replace('ie', 'ee')
            distorted = distorted.replace('ch', 'gh')
            distorted = distorted.replace('s', 'z')
            distorted = distorted.replace('r', 'rr')
            distorted = distorted.replace('u', 'uu')
            distorted = distorted.replace('w', 'f')
            
        return distorted.upper() + "!"

    def translate_word(self, word, lang_tag):
        if lang_tag == 'ork':
            return self.distort_orkish(word)
            
        if lang_tag not in self.languages:
            return word
            
        lang = self.languages[lang_tag]
        dict_data = lang.get('dictionary', {})
        rules = lang.get('rules', {})
        
        # Clean word
        clean_word = re.sub(r'[^\w\s\']', '', word).lower()
        
        # Suffix matching logic (e.g., word~suffix)
        suffix_map = rules.get('suffix', {})
        found_suffix = None
        base_word = clean_word
        
        for name, suff in suffix_map.items():
            if clean_word.endswith(suff):
                # Simple check: if removing suffix leaves a word in dictionary
                test_base = clean_word[:-len(suff)]
                if test_base in dict_data:
                    base_word = test_base
                    found_suffix = name
                    break
        
        translation = dict_data.get(base_word, f"<{word}?>")
        
        if found_suffix:
            translation = f"{translation}({found_suffix})"
            
        return translation

    def process_text(self, text):
        # Scan for tags [lang]...[/lang]
        pattern = r'\[(\w+)\](.*?)\[/\1\]'
        
        def replace_match(match):
            tag = match.group(1)
            content = match.group(2)
            words = content.split()
            translated_words = [self.translate_word(w, tag) for w in words]
            return " ".join(translated_words)

        return re.sub(pattern, replace_match, text, flags=re.DOTALL)

if __name__ == "__main__":
    translator_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(translator_dir, ".agent", "data", "languages")
    
    translator = SiebenwindTranslator(data_dir)
    
    if len(sys.argv) > 1:
        input_text = sys.argv[1]
        print(translator.process_text(input_text))
    else:
        print("Usage: python translator.py \"[run]Ich schreibe ein Buch[/run]\"")
