from pdf2image import convert_from_path
from PIL import Image, ImageChops, ImageFilter, ImageDraw, ImageFont
import tempfile
import os


def PDF_Comparator_images(new_img, old_img):
    # 差分を計算
    diff = ImageChops.difference(new_img, old_img).convert("L")
    # ノイズ除去
    mask = diff.point(lambda p: 255 if p > 10 else 0)
    # 膨張処理で差分領域を拡大
    mask = mask.filter(ImageFilter.MaxFilter(9))

    # 差分周辺を赤で塗ったマスク画像を作成
    red_overlay = Image.new("RGBA", mask.size, (255, 0, 0, 0))
    red_overlay.putalpha(mask.point(lambda p: int(0.5 * p)))

    # ハイライト画像を作成
    new_highlighted = Image.alpha_composite(new_img.convert("RGBA"), red_overlay)
    old_highlighted = Image.alpha_composite(old_img.convert("RGBA"), red_overlay)
    new_rgb = new_highlighted.convert("RGB")
    old_rgb = old_highlighted.convert("RGB")

    # 左上にラベルを追加
    new_draw = ImageDraw.Draw(new_rgb)
    old_draw = ImageDraw.Draw(old_rgb)
    new_draw.text((100, 100), "変更後", fill=(0, 0, 0, 255), font=ImageFont.truetype("meiryo.ttc", 100))
    old_draw.text((100, 100), "変更前", fill=(0, 0, 0, 255), font=ImageFont.truetype("meiryo.ttc", 100))

    return new_rgb, old_rgb


def PDF_Comparator(new_path, old_path):
    # PDFを画像として取得
    new_pages = [p.convert("RGB") for p in convert_from_path(new_path)]
    old_pages = [p.convert("RGB") for p in convert_from_path(old_path)]

    # ページ毎に比較する
    output_images = []
    for i in range(min(len(new_pages), len(old_pages))):
        new_rgb, old_rgb = PDF_Comparator_images(new_pages[i], old_pages[i])

        output_images.append(old_rgb)
        output_images.append(new_rgb)

    # PDF_Comparatorフォルダを一時ディレクトリ内に作成
    output_dir = os.path.join(tempfile.gettempdir(), "PDF_Comparator")
    os.makedirs(output_dir, exist_ok=True)

    # 結果をPDF保存
    new_name = os.path.basename(new_path).replace(".pdf", "")
    old_name = os.path.basename(old_path).replace(".pdf", "")
    output_path = os.path.join(output_dir, new_name + "__" + old_name + ".pdf")

    first, rest = output_images[0], output_images[1:]
    first.save(output_path, save_all=True, append_images=rest)
    return output_path


if __name__ == "__main__":
    # ================ 比較したいPDFのファイル名を入力してください ================
    new_pdf_path = "./sample/new.pdf"
    old_pdf_path = "./sample/old.pdf"
    # =========================================================================

    PDF_Comparator(new_pdf_path, old_pdf_path)
