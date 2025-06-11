# servidor.py (VERSÃO AJUSTADA PARA DEPLOY)

# --- Imports ---
import re
from collections import Counter
from mcp.server.fastmcp.prompts import base
from mcp.server.fastmcp import FastMCP, Context
import asyncio # Adicionado para a função assíncrona

# 1. Inicialize o Servidor para modo Web
# MUDANÇA: Adicionado stateless_http=True para otimizar para deploy web
mcp = FastMCP("MeuServidorMCP", stateless_http=True)
print(f"Servidor MCP '{mcp.name}' configurado para rodar via HTTP.")

# --- RESOURCES (Informações de Contexto para a IA) ---

@mcp.resource("meuMCP://about")
def get_assistant_capabilities() -> str:
    """Descreve as principais ferramentas e o propósito deste assistente."""
    print("-> Resource 'meuMCP://about' solicitado pelo cliente.")
    capabilities = """
    Eu sou um assistente de exemplo baseado no servidor 'MeuServidorMCP'. Minhas principais capacidades (ferramentas que posso usar) são:
    1.  **Contar Frequência de Palavras:** Analisar um texto e contar quantas vezes cada palavra aparece.
    2.  **Extrair URLs:** Encontrar links (http/https) dentro de um texto.
    3.  **Recomendar Site:** Posso te indicar um ótimo site para aprender sobre IA.
    4.  **Registrar Logs:** Posso registrar mensagens internamente (útil para depuração).

    Use-me para processar textos ou obter a recomendação do site!
    """
    print("   [meuMCP://about] Descrição das capacidades retornada.")
    return capabilities.strip()

# --- FERRAMENTAS (Tools - Ações que a IA pode chamar) ---

@mcp.tool()
def contar_frequencia_palavras(texto: str) -> str:
    """Conta a frequência de cada palavra em um texto fornecido."""
    print(f"-> Ferramenta 'contar_frequencia_palavras' chamada com texto: '{texto[:50]}...'")
    if not texto: return "Nenhum texto fornecido para análise."
    try:
        palavras = re.findall(r'\b\w+\b', texto.lower())
        if not palavras: return "Nenhuma palavra encontrada no texto."
        contagem = Counter(palavras)
        resultado_str = ", ".join([f"{palavra}: {freq}" for palavra, freq in contagem.most_common()])
        resultado = f"Frequência de palavras: {resultado_str}"
        print(f"   Resultado: {resultado}")
        return resultado
    except Exception as e:
        erro = f"Ocorreu um erro inesperado ao contar palavras: {e}"; print(f"   Erro: {erro}"); return erro
    
@mcp.tool()
def extrair_urls_texto(texto: str) -> str:
    """Encontra e lista todas as URLs (http ou https) dentro de um texto."""
    print(f"-> Ferramenta 'extrair_urls_texto' chamada com texto: '{texto[:50]}...'")
    if not texto: return "Nenhum texto fornecido para extrair URLs."
    try:
        urls_encontradas = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', texto)
        if urls_encontradas:
            resultado = f"URLs encontradas ({len(urls_encontradas)}): " + ", ".join(urls_encontradas)
        else:
            resultado = "Nenhuma URL encontrada no texto."
        print(f"   Resultado: {resultado}")
        return resultado
    except Exception as e:
        erro = f"Ocorreu um erro inesperado ao extrair URLs: {e}"; print(f"   Erro: {erro}"); return erro
    
# CORREÇÃO: A função agora é 'async' para usar 'await ctx.info'
@mcp.tool()
async def registrar_log_interno(mensagem: str, ctx: Context) -> str:
    """Registra uma mensagem nos logs internos do servidor MCP."""
    print(f"-> Ferramenta 'registrar_log_interno' chamada com mensagem: '{mensagem}'")
    # CORREÇÃO: 'await' é necessário para chamadas de I/O como log
    await ctx.info(f"Log via ferramenta: {mensagem}")
    resultado = f"Mensagem '{mensagem}' registrada nos logs."
    print(f"   Resultado: {resultado}")
    return resultado

# --- PROMPTS (Modelos de Conversa Iniciados pelo Usuário) ---
@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    """Inicia uma conversa para ajudar a depurar um erro."""
    print(f"-> Prompt 'debug_error' iniciado com erro: {error}")
    return [
        base.UserMessage(f"Estou recebendo este erro:\n```\n{error}\n```"),
        base.AssistantMessage("Entendido. Posso tentar ajudar a depurar. O que você já tentou fazer para resolver?"),
    ]

# Defina o bloco principal de execução para modo Web
if __name__ == "__main__":
    # MUDANÇA: Especificamos o transporte 'streamable-http' para rodar como um serviço web
    mcp.run(transport="streamable-http")
