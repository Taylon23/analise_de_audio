from translate import Translator
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# recursos necessários do NLTK
nltk.download('vader_lexicon')

def analisar_texto(texto_pt):
    translator = Translator(to_lang="en", from_lang="pt")
    texto_en = translator.translate(texto_pt)
    texto_principal = texto_en
    # Cria um objeto SentimentIntensityAnalyzer
    analisador = SentimentIntensityAnalyzer()
    print('Dados de sentimentos do texto extraido\n')
    # Analise de sentimento do texto traduzido
    sentimento = analisador.polarity_scores(texto_principal)
    
    return sentimento
