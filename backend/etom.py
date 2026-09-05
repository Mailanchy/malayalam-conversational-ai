import os
import boto3

class EnglishToMalayalamTranslator:
    def __init__(self):
        # Initialize AWS Translate client
        self.translate_client = boto3.client('translate',
            region_name='us-east-1',  # Replace with your AWS region
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),  # Your AWS access key
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")  # Your AWS secret key
        )

    def translate_to_malayalam(self, english_text):
        try:
            print(f"\n🌍 Translating to Malayalam: {english_text}")  # ✅ Debugging Output
            
            # Call AWS Translate
            response = self.translate_client.translate_text(
                Text=english_text,
                SourceLanguageCode='en',  # English
                TargetLanguageCode='ml'   # Malayalam
            )
            
            print("\n✅ Translation Successful!")  # ✅ Debugging Output
            return response['TranslatedText']
        
        except Exception as e:
            print(f"⚠ Translation error: {str(e)}")  # ✅ Debugging Output
            return "⚠ Translation failed"
