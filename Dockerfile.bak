FROM python:3.10-slim
WORKDIR /app
COPY web/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY web/ ./web/
COPY skills/ ./skills/
ENV GROQ_API_KEY=\"\"
ENV GROQ_MODEL=\"llama-3.3-70b-versatile\"
ENV GROQ_BASE_URL=\"https://api.groq.com/openai/v1\"
EXPOSE 7860
CMD [\"python\", \"web/app.py\"]
