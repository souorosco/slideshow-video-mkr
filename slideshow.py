#!/usr/bin/env python3
"""
slideshow.py — gera um vídeo tipo slideshow a partir das imagens de uma pasta.

Dependências:
  pip install moviepy imageio-ffmpeg

Exemplo de uso:
  python slideshow.py ~/imagens --output viagem.mp4 \
      --codec libx264 --resolution 1920x1080 --mode fit --duration 5

Parâmetros:
  input_dir    Pasta com as imagens.
  --output     Arquivo de saída (default slideshow.mp4).
  --codec      Codec FFMPEG (default libx264 / MP4 H.264).
  --resolution Resolução WxH (default 1920x1080).
  --mode       Tratamento de imagem: crop | fit | stretch (default fit).
  --duration   Tempo (s) que cada imagem permanece (default 10).
  --fps        FPS do vídeo final (default 24).
"""
import os
import re
import argparse
from typing import Tuple
from moviepy import ImageClip, ColorClip, CompositeVideoClip, concatenate_videoclips


def parse_resolution(res_str: str) -> Tuple[int, int]:
    match = re.match(r"(\d+)x(\d+)", res_str.lower())
    if not match:
        raise argparse.ArgumentTypeError(
            "Resolução deve estar no formato LARGURAxALTURA, por ex.: 1920x1080"
        )
    return int(match.group(1)), int(match.group(2))


def create_clip(path: str, duration: float, res: Tuple[int, int], mode: str):
    """Cria um ImageClip com o ajuste solicitado."""
    clip = ImageClip(path)
    W, H = res

    if mode == "fit":
        # Mantém proporção: dimensiona pela maior aresta e adiciona barras
        if W / clip.w < H / clip.h:
            clip = clip.resized(width=W)
        else:
            clip = clip.resized(height=H)
        # Cria fundo preto e posiciona a imagem no centro
        bg = ColorClip(res, color=(0, 0, 0)).with_duration(duration)
        clip = clip.with_position(("center", "center"))
        clip = CompositeVideoClip([bg, clip], size=res)


    elif mode == "stretch":
        # Estica ignorando proporção
        clip = clip.resized(new_size=res)

    elif mode == "crop":
        # Preenche toda a tela mantendo proporção e corta o excesso
        scale = max(W / clip.w, H / clip.h)
        clip = clip.resized(scale)
        clip = clip.cropped(
            x_center=clip.w / 2,
            y_center=clip.h / 2,
            width=W,
            height=H,
        )
    else:
        raise ValueError("mode deve ser crop, fit ou stretch")

    return clip.with_duration(duration)


def main():
    parser = argparse.ArgumentParser(description="Gere um slideshow em vídeo a partir das imagens de uma pasta.")
    parser.add_argument("input_dir", help="Diretório contendo as imagens")
    parser.add_argument("-o", "--output", default="slideshow.mp4", help="Arquivo de vídeo de saída")
    parser.add_argument(
        "--codec", default="libx264", help="Codec FFMPEG a ser usado (ex.: libx264, libx265, mpeg4)"
    )
    parser.add_argument(
        "--resolution",
        default="1920x1080",
        type=parse_resolution,
        help="Resolução de saída no formato LxA (ex.: 1280x720)",
    )
    parser.add_argument(
        "--mode", default="fit", choices=["crop", "fit", "stretch"], help="Modo de ajuste das imagens"
    )
    parser.add_argument("--duration", type=float, default=10.0, help="Duração em segundos de cada imagem")
    parser.add_argument("--fps", type=int, default=24, help="Frames por segundo do vídeo final")

    args = parser.parse_args()

    # Coleta e ordena as imagens
    valid_ext = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tif", ".tiff")
    images = [
        os.path.join(args.input_dir, f)
        for f in sorted(os.listdir(args.input_dir))
        if f.lower().endswith(valid_ext)
    ]

    if not images:
        raise SystemExit(f"Nenhuma imagem encontrada em {args.input_dir}")

    # Cria clipes individuais
    clips = [create_clip(p, args.duration, args.resolution, args.mode) for p in images]

    # Concatena e exporta
    video = concatenate_videoclips(clips, method="compose")
    video.write_videofile(args.output, fps=args.fps, codec=args.codec)


if __name__ == "__main__":
    main()
