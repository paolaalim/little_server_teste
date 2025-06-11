# servidor_web.py (VERSÃO CORRIGIDA)

# --- Imports ---
from mcp.server.fastmcp import FastMCP, Context
import asyncio # Precisamos importar asyncio para funções async

# --- 1. Inicialize o Servidor ---
mcp = FastMCP("MeuServidorWeb", stateless_http=True)
print(f"Servidor MCP '{mcp.name}' configurado para rodar via HTTP.")


# --- 2. Defina um RESOURCE (Informação de Contexto) ---
@mcp.resource("meuServidorWeb://about")
def get_server_description() -> str:
    """
    Descreve o propósito e as ferramentas deste servidor.
    Esta informação é lida pelo cliente MCP para entender as capacidades.
    """
    print("-> Resource 'meuServidorWeb://about' foi solicitado.")
    description = (
        "Olá! Eu sou um servidor MCP de exemplo, criado com o Parceiro de Programação.\n"
        "Minhas capacidades atuais incluem:\n"
        "1. **Saudação Personalizada:** Uma ferramenta que gera uma saudação para um nome específico."
    )
    return description


# --- 3. Defina uma TOOL (Ação que a IA pode chamar) ---
# MUDANÇA: A função agora é 'async def' para permitir o uso de 'await'
@mcp.tool()
async def saudacao_personalizada(nome: str, ctx: Context) -> str:
    """
    Gera uma mensagem de saudação calorosa para uma pessoa específica.

    :param nome: O nome da pessoa a ser saudada.
    :param ctx: O objeto de contexto do MCP, usado aqui para logar informações.
    """
    # MUDANÇA: Adicionado 'await' antes de ctx.info
    await ctx.info(f"-> Ferramenta 'saudacao_personalizada' chamada com o nome: {nome}")
    
    # MUDANÇA: Emoji removido para evitar o erro 'charmap' no console do Windows
    resultado = f"Olá, {nome}! Que seu dia seja repleto de código e sucesso!"
    
    print(f"Resultado da ferramenta: {resultado}")
    return resultado


# --- 4. Bloco Principal de Execução ---
if __name__ == "__main__":
    print("Iniciando o servidor em modo HTTP. Use 'mcp dev servidor_web.py' para testar.")
