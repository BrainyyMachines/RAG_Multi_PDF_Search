from utils import extract_text_from_pdf, split_text,build_faiss_index,search_chunks, get_answer_from_context,plot_vectors
from uuid import uuid4
import streamlit as st

st.set_page_config(page_title="🧠 AI Document Search Pro", layout="wide")
st.title("📄 AI-Powered Multi-PDF Search Engine")

uploaded_files = st.file_uploader("Upload one or more PDF documents", type="pdf", accept_multiple_files=True)
query = st.text_input("🔍 Ask something about the documents:")

if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = []
    
    
if uploaded_files:
    all_text = ""
    for file in uploaded_files:
        with open(f"temp_{uuid4()}.pdf", "wb") as f:
            f.write(file.read())
            text = extract_text_from_pdf(f.name)
            all_text += text + "\n"

    chunks = split_text(all_text)
    index, embeddings = build_faiss_index(chunks)

    st.success(f"{len(uploaded_files)} file(s) loaded and indexed successfully.")
    
if query:
        top_chunks, query_vector, retrieved_vectors = search_chunks(query, chunks, index, embeddings)
        context = "\n\n".join(top_chunks)
        answer = get_answer_from_context(query, context, st.session_state.chat_memory)

        st.markdown("### ✅ Answer:")
        st.write(answer)

        with st.expander("📜 Top Relevant Chunks"):
            for chunk in top_chunks:
                st.markdown(f"---\n{chunk}")

        with st.expander("📊 Vector Similarity Visualization"):
            plot_vectors(retrieved_vectors, query_vector)

        with st.expander("🧠 Conversation Memory"):
            st.json(st.session_state.chat_memory)
