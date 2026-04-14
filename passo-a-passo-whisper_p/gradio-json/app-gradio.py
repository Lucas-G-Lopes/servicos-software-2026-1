import html
import os

import gradio as gr
import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend-json:8080/validar-cpf")

CSS = """
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

:root {
    --bg: #f3f5f7;
    --panel: rgba(255, 255, 255, 0.94);
    --line: #cfd8df;
    --line-soft: #e6edf1;
    --text: #17303c;
    --muted: #5d7480;
    --brand: #0f766e;
    --valid-bg: #eaf8f1;
    --valid-line: #82c7a6;
    --invalid-bg: #fdf1e9;
    --invalid-line: #e4aa84;
    --warning-bg: #fcf6e2;
    --warning-line: #d8c16e;
    --error-bg: #f9ecef;
    --error-line: #d89aa6;
    --shadow: 0 22px 48px rgba(20, 43, 54, 0.08);
}

body,
.gradio-container {
    margin: 0;
    min-height: 100vh;
    font-family: 'IBM Plex Sans', sans-serif;
    color-scheme: light;
    color: var(--text);
    background:
        radial-gradient(circle at top, rgba(15, 118, 110, 0.06), transparent 24%),
        radial-gradient(circle at bottom right, rgba(18, 48, 60, 0.05), transparent 26%),
        linear-gradient(180deg, #f8fafb 0%, var(--bg) 100%);
}

.gradio-container,
.gradio-container .prose,
.gradio-container .prose p,
.gradio-container .prose h1,
.gradio-container .prose h2,
.gradio-container label,
.gradio-container input,
.gradio-container textarea,
.gradio-container strong,
.gradio-container span,
.gradio-container div {
    color: var(--text);
}

#app-shell {
    max-width: 760px;
    margin: 0 auto;
    padding: 64px 20px 40px;
}

.app-card {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 24px;
    box-shadow: var(--shadow);
    backdrop-filter: blur(10px);
    padding: 28px;
}

.app-header {
    margin-bottom: 18px;
}

.app-header h1 {
    margin: 0 0 8px;
    font-size: 2rem;
    line-height: 1.1;
}

.app-header p {
    margin: 0;
    color: var(--muted);
    line-height: 1.6;
}

#cpf-input textarea,
#cpf-input input {
    border-radius: 16px !important;
    border: 1px solid var(--line) !important;
    background: linear-gradient(180deg, #ffffff 0%, #fbfdfe 100%) !important;
    color: var(--text) !important;
    font-size: 1.05rem !important;
    padding: 15px 16px !important;
    min-height: 56px !important;
    box-shadow:
        0 1px 2px rgba(17, 35, 44, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.85) !important;
}

#cpf-input,
#cpf-input > div,
#cpf-input > div > div {
    background: transparent !important;
    box-shadow: none !important;
}

#cpf-input > div,
#cpf-input > div > div {
    border: none !important;
}

#cpf-input textarea:focus,
#cpf-input input:focus {
    border-color: rgba(15, 118, 110, 0.55) !important;
    box-shadow:
        0 0 0 4px rgba(15, 118, 110, 0.12),
        0 10px 24px rgba(15, 118, 110, 0.08) !important;
    outline: none !important;
}

#cpf-input label {
    font-weight: 600 !important;
    color: var(--text) !important;
    margin-bottom: 8px !important;
}

#cpf-input input::placeholder,
#cpf-input textarea::placeholder {
    color: #8ba0ab !important;
    opacity: 1 !important;
}

.result-card {
    margin-top: 18px;
    border-radius: 18px;
    border: 1px solid var(--line);
    background: #f8fbfc;
    padding: 18px;
}

.result-card.is-valid {
    background: var(--valid-bg);
    border-color: var(--valid-line);
}

.result-card.is-invalid {
    background: var(--invalid-bg);
    border-color: var(--invalid-line);
}

.result-card.is-warning {
    background: var(--warning-bg);
    border-color: var(--warning-line);
}

.result-card.is-error {
    background: var(--error-bg);
    border-color: var(--error-line);
}

.result-status {
    display: inline-flex;
    align-items: center;
    margin-bottom: 10px;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--text);
    background: rgba(255, 255, 255, 0.86);
    border: 1px solid var(--line-soft);
}

.result-title {
    margin: 0 0 8px;
    font-size: 1.1rem;
    color: var(--text);
}

.result-message {
    margin: 0 0 14px;
    color: var(--muted);
    line-height: 1.6;
}

.result-grid {
    display: grid;
    gap: 10px;
}

.result-item {
    display: grid;
    gap: 4px;
    padding: 12px 14px;
    border-radius: 14px;
    background: rgba(255, 255, 255, 0.82);
    border: 1px solid rgba(207, 216, 223, 0.85);
}

.result-item span {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--muted);
}

.result-item strong {
    font-size: 0.98rem;
    line-height: 1.45;
    word-break: break-word;
    color: var(--text);
}

footer {
    display: none !important;
}

@media (max-width: 640px) {
    #app-shell {
        padding: 28px 14px 28px;
    }

    .app-card {
        padding: 20px;
        border-radius: 20px;
    }

    .app-header h1 {
        font-size: 1.7rem;
    }
}
"""


def render_resultado(
    *,
    titulo: str,
    status: str,
    mensagem: str,
    cpf_informado: str,
    cpf_normalizado: str,
    cpf_formatado: str,
) -> str:
    return f"""
    <div class="result-card {status}">
      <div class="result-status">{html.escape(titulo)}</div>
      <h2 class="result-title">{html.escape(titulo)}</h2>
      <p class="result-message">{html.escape(mensagem)}</p>
      <div class="result-grid">
        <div class="result-item">
          <span>CPF informado</span>
          <strong>{html.escape(cpf_informado or 'Nao informado')}</strong>
        </div>
        <div class="result-item">
          <span>CPF normalizado</span>
          <strong>{html.escape(cpf_normalizado or 'Sem digitos reconhecidos')}</strong>
        </div>
        <div class="result-item">
          <span>CPF formatado</span>
          <strong>{html.escape(cpf_formatado or 'Indisponivel')}</strong>
        </div>
      </div>
    </div>
    """


def render_resultado_inicial() -> str:
    return render_resultado(
        titulo="Aguardando consulta",
        status="is-warning",
        mensagem="Digite um CPF e pressione Enter para validar.",
        cpf_informado="",
        cpf_normalizado="",
        cpf_formatado="",
    )


def validar_cpf(cpf: str) -> str:
    if not cpf or not cpf.strip():
        return render_resultado(
            titulo="Preencha o campo",
            status="is-warning",
            mensagem="Informe um CPF para iniciar a validacao.",
            cpf_informado="",
            cpf_normalizado="",
            cpf_formatado="",
        )

    try:
        response = requests.post(BACKEND_URL, json={"cpf": cpf}, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        return render_resultado(
            titulo="Falha de conexao",
            status="is-error",
            mensagem=f"Nao foi possivel consultar o backend no momento. Detalhe: {exc}",
            cpf_informado=cpf,
            cpf_normalizado="",
            cpf_formatado="",
        )

    resultado = response.json()
    return render_resultado(
        titulo="CPF valido" if resultado["valido"] else "CPF invalido",
        status="is-valid" if resultado["valido"] else "is-invalid",
        mensagem=resultado["mensagem"],
        cpf_informado=resultado["cpf_informado"],
        cpf_normalizado=resultado["cpf_normalizado"],
        cpf_formatado=resultado["cpf_formatado"] or "",
    )


with gr.Blocks(title="Validador de CPF") as demo:
    with gr.Column(elem_id="app-shell"):
        with gr.Column(elem_classes=["app-card"]):
            gr.HTML(
                """
                <div class="app-header">
                  <h1>Validador de CPF</h1>
                  <p>Consulte um CPF com ou sem pontuacao e veja o resultado logo abaixo.</p>
                </div>
                """
            )

            cpf_input = gr.Textbox(
                label="CPF",
                placeholder="Ex.: 529.982.247-25",
                info="Digite com ou sem pontuacao e pressione Enter para validar.",
                lines=1,
                elem_id="cpf-input",
            )

            resultado = gr.HTML(value=render_resultado_inicial())

    cpf_input.submit(fn=validar_cpf, inputs=cpf_input, outputs=resultado)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, css=CSS)
