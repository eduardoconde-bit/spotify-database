FROM alpine:latest

# Instalar pacotes essenciais
RUN apk update && apk add --no-cache \
    curl \
    git \
    bash \
    zsh \
    nano \
    vim \
    mariadb-client \
    python3 \
    py3-pip \
    nodejs \
    npm

# Criar diretório de trabalho
WORKDIR /workspace

# Configurar shell
RUN echo "alias ll='ls -la'" >> ~/.bashrc

CMD ["sleep", "infinity"]
