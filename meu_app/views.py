import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

# Função que treina o modelo de KNN
def treinar_modelo_knn(df):
    # Remover colunas não numéricas, como 'Nome'
    df = df.select_dtypes(include=['number'])  # Mantém apenas as colunas numéricas
    
    # Aqui, 'Alvo' é a variável dependente
    X = df.drop(columns=['Alvo'])  # Excluindo a coluna alvo
    y = df['Alvo']  # Coluna alvo
    
    # Dividindo os dados em treino e teste (80% treino, 20% teste)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Normalizando os dados
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    # Inicializando o KNN com k=3
    knn = KNeighborsClassifier(n_neighbors=3)
    
    # Treinando o modelo
    knn.fit(X_train, y_train)
    
    # Realizando predições
    y_pred = knn.predict(X_test)
    
    # Calculando a precisão (accuracy)
    accuracy = accuracy_score(y_test, y_pred)
    
    return knn, accuracy


# Função que carrega os dados e exibe os resultados
def carregar_dados(request):
    if request.method == 'POST' and request.FILES['arquivo']:
        arquivo = request.FILES['arquivo']
        
        try:
            # Carregar o CSV
            df = pd.read_csv(arquivo, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(arquivo, encoding='latin1')  # Caso o arquivo use Latin-1
        
        # Verificar se a coluna 'Alvo' existe
        if 'Alvo' not in df.columns:
            return HttpResponse(f"Erro: A coluna 'Alvo' não foi encontrada no arquivo. As colunas disponíveis são: {df.columns}.", status=400)
        
        # Treinando o modelo de KNN
        modelo, accuracy = treinar_modelo_knn(df)
        
        # Formatar a precisão para exibição (em porcentagem com 2 casas decimais)
        accuracy_percent = f"{accuracy * 100:.2f}"
        
        # Exibindo os resultados
        estatisticas = df.describe().to_html()
        
        # Convertendo o DataFrame para HTML
        tabela_html = df.to_html(index=False)
        
        return render(request, 'meu_app/resultados.html', {
            'tabela': tabela_html,
            'estatisticas': estatisticas,
            'accuracy': accuracy_percent  # Passando a precisão já formatada
        })
    
    return render(request, 'meu_app/upload.html')
