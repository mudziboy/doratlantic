<!-- ⚡ DOR ATLANTIC BOT README.md with Canvas for Easy Copy ⚡ -->
<div align="center">
  <canvas id="readmeCanvas" width="900" height="1300" style="border:1px solid #ddd; border-radius: 10px; box-shadow: 0 5px 25px rgba(0,0,0,0.1);"></canvas>
</div>

<script>
  const canvas = document.getElementById('readmeCanvas');
  const ctx = canvas.getContext('2d');

  // Styles
  const titleFont = "bold 28px Arial";
  const subtitleFont = "bold 18px Arial";
  const normalFont = "16px Arial";
  const lineHeight = 26;
  const marginX = 20;
  let posY = 40;

  // Draw title
  ctx.font = titleFont;
  ctx.fillStyle = "#d32f2f";
  ctx.textAlign = "center";
  ctx.fillText("🔥 DOR ATLANTIC BOT 🔥", canvas.width / 2, posY);

  // Banner Image
  const img = new Image();
  img.crossOrigin = 'anonymous';
  img.onload = () => {
    ctx.drawImage(img, canvas.width / 2 - 360, posY + 10, 720, 160);

    // After image loaded, draw rest of content
    posY += 190;
    drawContent();
  };
  img.src = "https://raw.githubusercontent.com/mudziboy/doratlantic/main/app/botdor.jpg";

  function drawTextBlock(text, font = normalFont, color = "#000") {
    ctx.font = font;
    ctx.fillStyle = color;
    ctx.textAlign = "left";
    const maxWidth = canvas.width - marginX * 2;
    let words = text.split(' ');
    let line = '';
    for(let n = 0; n < words.length; n++) {
      const testLine = line + words[n] + ' ';
      const metrics = ctx.measureText(testLine);
      const testWidth = metrics.width;
      if (testWidth > maxWidth && n > 0) {
        ctx.fillText(line, marginX, posY);
        line = words[n] + ' ';
        posY += lineHeight;
      } else {
        line = testLine;
      }
    }
    ctx.fillText(line, marginX, posY);
    posY += lineHeight + 10;
  }

  function drawList(items, bullet = "•", color = "#000") {
    ctx.font = normalFont;
    ctx.fillStyle = color;
    ctx.textAlign = "left";
    const maxWidth = canvas.width - marginX * 3;
    items.forEach(item => {
      let lines = wrapText(item.text, maxWidth);
      lines.forEach((line, i) => {
        const prefix = i === 0 ? bullet + " " : "  ";
        ctx.fillText(prefix + line, marginX + 15, posY);
        posY += lineHeight;
      });
      posY += 5;
    });
    posY += 10;
  }

  function wrapText(text, maxWidth) {
    let words = text.split(' ');
    let lines = [];
    let line = '';
    let testLine;
    while(words.length > 0) {
      testLine = line + words[0] + ' ';
      let metrics = ctx.measureText(testLine);
      if(metrics.width > maxWidth && line !== '') {
        lines.push(line.trim());
        line = '';
      } else {
        line = testLine;
        words.shift();
      }
    }
    if(line) lines.push(line.trim());
    return lines;
  }

  function drawContent() {
    // Table of Contents
    ctx.font = subtitleFont;
    ctx.fillStyle = "#b71c1c";
    ctx.fillText("📖 DAFTAR ISI", marginX, posY);
    posY += lineHeight;

    drawList([
      { text: "💡 Tentang Proyek" },
      { text: "🚀 Instalasi Cepat" },
      { text: "💳 Integrasi Pembayaran" },
      { text: "🖼️ Pratinjau Bot" },
      { text: "🙏 Ucapan Terima Kasih" },
      { text: "📞 Kontak & Versi Penuh" },
    ]);

    // Tentang Proyek
    ctx.font = subtitleFont;
    ctx.fillStyle = "#b71c1c";
    ctx.fillText("💡 TENTANG PROYEK", marginX, posY);
    posY += lineHeight;

    drawTextBlock("DOR ATLANTIC BOT adalah solusi Telegram Bot yang ringkas dan efisien, dirancang khusus untuk mengotomatisasi layanan pembelian paket data XL Provider dan berbagai layanan PPOB (Payment Point Online Bank). Inti dari bot ini adalah integrasi penuh dengan Payment Gateway terkemuka, Atlantic Pedia.");

    // Fitur Utama
    ctx.font = subtitleFont;
    ctx.fillStyle = "#b71c1c";
    ctx.fillText("Fitur Utama", marginX, posY);
    posY += lineHeight;

    const features = [
      { text: "🔑 Manajemen Akun — Sistem Login dan pendaftaran pengguna bot yang aman." },
      { text: "💰 Top Up Otomatis — Proses pengisian saldo PPOB yang cepat dan terintegrasi." },
      { text: "📦 Transaksi PPOB — Pembelian pulsa, paket data XL, token listrik, dan layanan PPOB lainnya." },
      { text: "⚙️ Telegram API — Interaksi real-time dengan pengguna melalui Telegram Bot API." },
    ];
    drawList(features);

    // Instalasi Cepat
    ctx.font = subtitleFont;
    ctx.fillStyle = "#b71c1c";
    ctx.fillText("🚀 INSTALASI CEPAT", marginX, posY);
    posY += lineHeight;

    drawTextBlock(`Untuk menjalankan versi dasar dari DOR ATLANTIC BOT, ikuti langkah-langkah instalasi otomatis berikut:`);
    ctx.font = '16px monospace';
    ctx.fillStyle = "#444";
    const installCmd = [
      '# Unduh script instalasi',
      'wget https://github.com/mudziboy/doratlantic/raw/refs/heads/main/install-bot',
      '',
      '# Berikan izin eksekusi',
      'chmod +x install-bot',
      '',
      '# Jalankan instalasi',
      './install-bot'
    ];
    installCmd.forEach(line => {
      ctx.fillText(line, marginX+10, posY);
      posY += lineHeight;
    });

    ctx.font = subtitleFont;
    ctx.fillStyle = "#d32f2f";
    posY += 10;
    ctx.fillText("[!WARNING] ⚠️ Perhatian Penting", marginX, posY);
    posY += lineHeight;

    ctx.font = normalFont;
    ctx.fillStyle = "#000";
    drawTextBlock("Script di repositori ini masih dalam tahap pengembangan aktif (Under Development). Beberapa fungsi mungkin memerlukan penyesuaian, konfigurasi manual, dan proses debugging untuk dapat berjalan optimal.");

    // Integrasi Pembayaran
    ctx.font = subtitleFont;
    ctx.fillStyle = "#b71c1c";
    ctx.fillText("💳 INTEGRASI PEMBAYARAN", marginX, posY);
    posY += lineHeight;

    drawTextBlock("DOR ATLANTIC BOT dibangun dengan fokus pada efisiensi transaksi.");
    drawTextBlock("✅ Atlantic Pedia Payment Gateway
Script ini sudah mendukung sistem pembayaran langsung dari Atlantic Pedia. Hal ini memungkinkan pembelian otomatis dengan saldo PPOB yang tersedia atau melalui metode pembayaran yang terdaftar di Atlantic Pedia.");

    // Pratinjau Bot
    ctx.font = subtitleFont;
    ctx.fillStyle = "#b71c1c";
    ctx.fillText("🖼️ PRATINJAU BOT", marginX, posY);
    posY += lineHeight;

    drawTextBlock("Lihat bagaimana bot ini berinteraksi dengan pengguna:");

    // Images Preview (small thumbnails)
    const previewImages = [
      "https://raw.githubusercontent.com/mudziboy/doratlantic/main/app/botdor.jpg",
      "https://raw.githubusercontent.com/mudziboy/doratlantic/main/app/botdor2.jpg",
      "https://raw.githubusercontent.com/mudziboy/doratlantic/main/app/botdor1.jpg",
    ];

    // Draw preview thumbnails
    let xThumb = marginX;
    let yThumb = posY + 10;
    let thumbSize = 120;
    previewImages.forEach(src => {
      let imgThumb = new Image();
      imgThumb.crossOrigin = "anonymous";
      imgThumb.src = src;
      imgThumb.onload = () => {
        ctx.drawImage(imgThumb, xThumb, yThumb, thumbSize, thumbSize * (imgThumb.height / imgThumb.width));
      };
      xThumb += thumbSize + 15;
    });

    posY = yThumb + thumbSize + 40;
    ctx.font = subtitleFont;
    ctx.fillStyle = "#d32f2f";
    ctx.fillText("🔗 COBA DEMO BOT KAMI DI TELEGRAM: t.me/dorinajabot", marginX, posY);

    // Ucapan Terima Kasih
    posY += lineHeight * 2;
    ctx.font = subtitleFont;
    ctx.fillStyle = "#b71c1c";
    ctx.fillText("🙏 UCAPAN TERIMA KASIH", marginX, posY);
    posY += lineHeight;

    drawTextBlock("Kami mengucapkan penghargaan setinggi-tingginya kepada para kontributor dan inspirator proyek ini:
Fuyuki, Maha Guru Komunitas Taman Kanak-kanak FuyukiXT: Atas base script awal yang menjadi pondasi dari proyek ini.
Gemini, AI dari Google: Atas bantuan yang tak ternilai dalam proses pengembangan dan coding proyek "Ragumu Rugimu Raimu" ini.");

    // Kontak & Versi Penuh
    posY += 10;
    ctx.font = subtitleFont;
    ctx.fillStyle = "#b71c1c";
    ctx.fillText("📞 KONTAK & VERSI PENUH", marginX, posY);
    posY += lineHeight;

    drawTextBlock("Butuh script yang utuh, siap pakai, dan sudah teruji? Silakan hubungi kami untuk mendapatkan versi lengkap dan stabil dari DOR ATLANTIC BOT serta layanan instalasi dan kustomisasi.");

    // Contact Badge
    let contactImg = new Image();
    contactImg.crossOrigin = "anonymous";
    contactImg.onload = () => {
      ctx.drawImage(contactImg, marginX, posY, 250, 50);
      posY += 70;

      // Footer
      ctx.font = "14px Arial";
      ctx.fillStyle = "#888";
      ctx.textAlign = "center";
      ctx.fillText("Made with ❤️ by mudziboy© 2025 — DOR FT TUNNEL PROJECT", canvas.width/2, posY);
    };
    contactImg.src = "https://img.shields.io/badge/Contact%20Creator-mudziboy-red?style=for-the-badge&logo=telegram&logoColor=white";
  }
</script>
