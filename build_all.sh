#!/bin/bash

# List of source files
SRC_FILES=("bot.c" "socket/tcp_socket.c")

OUTPUT_DIR="binarios"
COMPILERS_DIR="compilers_extracted"

mkdir -p "$OUTPUT_DIR"

# Check if any source file uses pthread
USES_PTHREAD="no"
for SRC in "${SRC_FILES[@]}"; do
    if grep -q "pthread_" "$SRC"; then
        USES_PTHREAD="yes"
        break
    fi
done

# Combine all source files into a single string for GCC
SRC_LIST=$(printf " %s" "${SRC_FILES[@]}")

for dir in "$COMPILERS_DIR"/*; do
    if [[ -d "$dir" ]]; then
        BIN_PATH=$(find "$dir" -type f -executable -name "*-gcc" | head -n 1)

        if [[ -n "$BIN_PATH" ]]; then
            ARCH=$(basename "$dir" | sed 's/cross-compiler-//')
            OUTFILE="$OUTPUT_DIR/bot.$ARCH"

            echo "[+] Compilando para $ARCH..."

            if [[ "$USES_PTHREAD" == "yes" ]]; then
                "$BIN_PATH" -std=c99 -static -w $SRC_LIST -o "$OUTFILE" -lpthread
            else
                "$BIN_PATH" -std=c99 -static -w $SRC_LIST -o "$OUTFILE"
            fi

            if [[ $? -eq 0 ]]; then
                echo "[✔] Sucesso: $OUTFILE"
            else
                echo "[✘] Falha ao compilar para $ARCH"
            fi
        else
            echo "[!] GCC não encontrado em: $dir"
        fi
    fi
done