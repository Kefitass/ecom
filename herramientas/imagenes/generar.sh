#!/usr/bin/env bash
# Regenera todas las imágenes de las marcas.
set -e
cd "$(dirname "$0")/../.."
export BUILD_DIR=${BUILD_DIR:-/tmp/imagenes-build}
python3 herramientas/imagenes/generar_imagenes.py
PW=${PW:-$(npm root -g)/playwright} node herramientas/imagenes/render.js "$BUILD_DIR/jobs.json"
