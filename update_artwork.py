import json

with open('events/artwork_data.json') as f:
    photos = json.load(f)

# Sort descending by timestamp (newest first)
photos_sorted = sorted(photos, key=lambda x: x['timestamp'], reverse=True)
total_count = len(photos_sorted)

# Collect years and counts
years_order = []
for p in photos_sorted:
    y = p['year']
    if y not in years_order:
        years_order.append(y)

photos_json_str = json.dumps(photos_sorted)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Artwork Gallery | Amio Sarker</title>
  <style>
    * {{
      box-sizing: border-box;
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      margin: 0;
      padding: 0;
      background: #f8fafc;
      color: #1e293b;
      line-height: 1.6;
    }}

    /* Header */
    header {{
      background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
      color: white;
      padding: 40px 20px 30px 20px;
      text-align: center;
      border-bottom: 3px solid #3b82f6;
    }}

    header h1 {{
      margin: 0 0 10px 0;
      font-size: 2.2rem;
      letter-spacing: -0.5px;
    }}

    header p {{
      margin: 0;
      color: #94a3b8;
      font-size: 1.1rem;
      max-width: 650px;
      margin: 0 auto;
    }}

    /* Navigation */
    nav {{
      display: flex;
      justify-content: center;
      background: #334155;
      position: sticky;
      top: 0;
      z-index: 100;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }}

    nav a {{
      color: #f1f5f9;
      padding: 14px 24px;
      display: inline-block;
      text-decoration: none;
      font-weight: 500;
      transition: background 0.2s ease, color 0.2s ease;
    }}

    nav a:hover, nav a.active {{
      background: #475569;
      color: #38bdf8;
    }}

    .container {{
      max-width: 1280px;
      margin: 35px auto;
      padding: 0 20px 80px 20px;
    }}

    /* Custom Scrollbar Styling */
    .custom-scrollbar::-webkit-scrollbar {{
      height: 10px;
      width: 10px;
    }}
    .custom-scrollbar::-webkit-scrollbar-track {{
      background: #e2e8f0;
      border-radius: 9999px;
    }}
    .custom-scrollbar::-webkit-scrollbar-thumb {{
      background: #3b82f6;
      border-radius: 9999px;
      border: 2px solid #e2e8f0;
    }}
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {{
      background: #1d4ed8;
    }}

    /* Horizontal Filmstrip Timeline Section */
    .reel-section {{
      background: white;
      border: 1px solid #e2e8f0;
      border-radius: 14px;
      padding: 24px;
      margin-bottom: 35px;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
    }}

    .reel-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
      flex-wrap: wrap;
      gap: 10px;
    }}

    .reel-header h2 {{
      margin: 0;
      font-size: 1.35rem;
      color: #0f172a;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .reel-hint {{
      color: #64748b;
      font-size: 0.88rem;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .reel-scroll-container {{
      display: flex;
      gap: 16px;
      overflow-x: auto;
      padding-bottom: 14px;
      scroll-behavior: smooth;
      -webkit-overflow-scrolling: touch;
    }}

    .reel-item {{
      flex: 0 0 200px;
      height: 160px;
      position: relative;
      border-radius: 10px;
      overflow: hidden;
      background: #0f172a;
      cursor: pointer;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
      transition: transform 0.25s ease, box-shadow 0.25s ease;
    }}

    .reel-item:hover {{
      transform: translateY(-4px) scale(1.02);
      box-shadow: 0 8px 18px rgba(0, 0, 0, 0.15);
    }}

    .reel-item img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.3s ease;
    }}

    .reel-item:hover img {{
      transform: scale(1.08);
    }}

    .reel-date-overlay {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      padding: 8px 10px;
      background: linear-gradient(to top, rgba(15, 23, 42, 0.95), rgba(15, 23, 42, 0.5) 60%, transparent);
      color: white;
      font-size: 0.78rem;
      font-weight: 600;
      opacity: 0;
      transform: translateY(6px);
      transition: opacity 0.2s ease, transform 0.2s ease;
      pointer-events: none;
      text-align: center;
    }}

    .reel-item:hover .reel-date-overlay {{
      opacity: 1;
      transform: translateY(0);
    }}

    /* Filter & Controls Toolbar */
    .toolbar {{
      background: white;
      border: 1px solid #e2e8f0;
      border-radius: 12px;
      padding: 16px 20px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
      margin-bottom: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    .toolbar-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}

    .counter-badge {{
      font-size: 0.95rem;
      color: #334155;
      font-weight: 600;
    }}

    .album-link {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 15px;
      background: #eff6ff;
      color: #2563eb;
      border: 1px solid #bfdbfe;
      border-radius: 8px;
      font-size: 0.88rem;
      font-weight: 600;
      text-decoration: none;
      transition: background 0.2s ease;
    }}

    .album-link:hover {{
      background: #dbeafe;
    }}

    .filters-wrapper {{
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 6px;
      -webkit-overflow-scrolling: touch;
    }}

    .filter-btn {{
      background: #f1f5f9;
      color: #475569;
      border: 1px solid #e2e8f0;
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 0.86rem;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s ease;
      flex-shrink: 0;
    }}

    .filter-btn:hover {{
      background: #e2e8f0;
      color: #0f172a;
    }}

    .filter-btn.active {{
      background: #2563eb;
      color: white;
      border-color: #2563eb;
    }}

    /* Main Scrollable Gallery Window */
    .grid-wrapper {{
      background: white;
      border: 1px solid #e2e8f0;
      border-radius: 14px;
      padding: 24px;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
      max-height: 860px;
      overflow-y: auto;
    }}

    .gallery-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 20px;
    }}

    .art-card {{
      position: relative;
      border-radius: 12px;
      overflow: hidden;
      background: #0f172a;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
      border: 1px solid #e2e8f0;
      cursor: pointer;
      aspect-ratio: 4 / 3;
      content-visibility: auto;
      contain-intrinsic-size: 260px 195px;
      transition: transform 0.25s ease, box-shadow 0.25s ease;
    }}

    .art-card:hover {{
      transform: translateY(-5px);
      box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    }}

    .art-card img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: transform 0.35s ease, filter 0.25s ease;
    }}

    .art-card:hover img {{
      transform: scale(1.06);
      filter: brightness(0.92);
    }}

    /* Date Overlay on Hover */
    .date-overlay {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      padding: 14px 16px;
      background: linear-gradient(to top, rgba(15, 23, 42, 0.95) 0%, rgba(15, 23, 42, 0.6) 60%, transparent 100%);
      color: white;
      font-size: 0.92rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
      opacity: 0;
      transform: translateY(8px);
      transition: opacity 0.25s ease, transform 0.25s ease;
      pointer-events: none;
    }}

    .art-card:hover .date-overlay {{
      opacity: 1;
      transform: translateY(0);
    }}

    .date-pill {{
      background: rgba(37, 99, 235, 0.88);
      backdrop-filter: blur(4px);
      padding: 4px 12px;
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 700;
      letter-spacing: 0.3px;
    }}

    /* Fullscreen Lightbox Modal */
    .modal {{
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(8px);
      z-index: 1000;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      padding: 20px;
    }}

    .modal.active {{
      display: flex;
    }}

    .modal-img-container {{
      position: relative;
      max-width: 90vw;
      max-height: 80vh;
      display: flex;
      justify-content: center;
      align-items: center;
    }}

    .modal-img-container img {{
      max-width: 100%;
      max-height: 80vh;
      border-radius: 8px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
      object-fit: contain;
    }}

    .modal-caption {{
      margin-top: 16px;
      color: white;
      font-size: 1.1rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .modal-close {{
      position: absolute;
      top: 20px;
      right: 25px;
      color: white;
      font-size: 2.2rem;
      background: none;
      border: none;
      cursor: pointer;
      line-height: 1;
      opacity: 0.8;
      transition: opacity 0.2s ease, transform 0.2s ease;
    }}

    .modal-close:hover {{
      opacity: 1;
      transform: scale(1.1);
    }}

    .modal-nav-btn {{
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      background: rgba(255, 255, 255, 0.15);
      color: white;
      border: none;
      font-size: 1.8rem;
      width: 48px;
      height: 48px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: background 0.2s ease;
    }}

    .modal-nav-btn:hover {{
      background: rgba(255, 255, 255, 0.3);
    }}

    .modal-prev {{
      left: 20px;
    }}

    .modal-next {{
      right: 20px;
    }}

    @media (max-width: 640px) {{
      .gallery-grid {{
        grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
        gap: 12px;
      }}
      .modal-nav-btn {{
        width: 36px;
        height: 36px;
        font-size: 1.4rem;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Artwork & Creative Gallery</h1>
    <p>A collection of {total_count} creative artworks spanning from 2016 to 2026.</p>
  </header>

  <nav>
    <a href="index.html">All Projects</a>
    <a href="events/events.html">Events</a>
    <a href="artwork.html" class="active">Artwork</a>
  </nav>

  <div class="container">
    <!-- Horizontal Filmstrip Timeline Reel with Custom Scrollbar -->
    <div class="reel-section">
      <div class="reel-header">
        <h2>🎨 Highlights Timeline</h2>
        <span class="reel-hint">Scroll horizontally or drag the scroll bar &rarr;</span>
      </div>
      <div class="reel-scroll-container custom-scrollbar" id="reelContainer">
        <!-- Populated via JavaScript -->
      </div>
    </div>

    <!-- Toolbar: Year Filters, Counter & External Link -->
    <div class="toolbar">
      <div class="toolbar-top">
        <span class="counter-badge" id="counterText">Showing {total_count} of {total_count} artworks</span>
        <a href="https://photos.app.goo.gl/PTPqHTXI8TZDvjJP2" target="_blank" rel="noopener" class="album-link">
          🖼️ Open in Google Photos &nearr;
        </a>
      </div>

      <div class="filters-wrapper custom-scrollbar" id="filtersContainer">
        <!-- Filter buttons populated via JavaScript -->
      </div>
    </div>

    <!-- Main Scrollable Gallery Window with Custom Scrollbar -->
    <div class="grid-wrapper custom-scrollbar">
      <div class="gallery-grid" id="galleryGrid">
        <!-- Populated via JavaScript -->
      </div>
    </div>
  </div>

  <!-- Fullscreen Modal Lightbox -->
  <div class="modal" id="imageModal">
    <button class="modal-close" id="modalClose">&times;</button>
    <button class="modal-nav-btn modal-prev" id="modalPrev">&larr;</button>
    <button class="modal-nav-btn modal-next" id="modalNext">&rarr;</button>
    <div class="modal-img-container">
      <img id="modalImg" src="" alt="Enlarged artwork" />
    </div>
    <div class="modal-caption" id="modalCaption"></div>
  </div>

  <script>
    const allPhotos = {photos_json_str};
    let currentPhotos = [...allPhotos];
    let currentIndex = 0;

    const galleryGrid = document.getElementById('galleryGrid');
    const reelContainer = document.getElementById('reelContainer');
    const counterText = document.getElementById('counterText');
    const filtersContainer = document.getElementById('filtersContainer');

    // Build Dynamic Year Filters
    function setupFilters() {{
      const yearCounts = {{}};
      allPhotos.forEach(p => {{
        yearCounts[p.year] = (yearCounts[p.year] || 0) + 1;
      }});

      const sortedYears = Object.keys(yearCounts).sort((a, b) => b.localeCompare(a));

      let filtersHtml = `<button class="filter-btn active" data-year="all">All Years (${{allPhotos.length}})</button>`;
      sortedYears.forEach(year => {{
        filtersHtml += `<button class="filter-btn" data-year="${{year}}">${{year}} (${{yearCounts[year]}})</button>`;
      }});

      filtersContainer.innerHTML = filtersHtml;

      filtersContainer.querySelectorAll('.filter-btn').forEach(btn => {{
        btn.addEventListener('click', () => {{
          filtersContainer.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          const year = btn.getAttribute('data-year');
          if (year === 'all') {{
            currentPhotos = [...allPhotos];
          }} else {{
            currentPhotos = allPhotos.filter(p => p.year === year);
          }}
          renderGallery(currentPhotos);
        }});
      }});
    }}

    // Populate Horizontal Reel (sample highlights across the collection)
    function renderReel() {{
      const step = Math.max(1, Math.floor(allPhotos.length / 40));
      const reelPhotos = allPhotos.filter((_, i) => i % step === 0);

      reelContainer.innerHTML = reelPhotos.map(photo => `
        <div class="reel-item" onclick="openModalByPhotoId('${{photo.id}}')" title="Created on ${{photo.date}}">
          <img src="${{photo.baseUrl}}=w400-h300-c" alt="Artwork created on ${{photo.date}}" loading="lazy" />
          <div class="reel-date-overlay">📅 ${{photo.date}}</div>
        </div>
      `).join('');
    }}

    // Populate Main Gallery Grid
    function renderGallery(photosToRender) {{
      galleryGrid.innerHTML = photosToRender.map((photo, index) => `
        <div class="art-card" onclick="openModal(${{index}})" title="Created on ${{photo.date}}">
          <img src="${{photo.baseUrl}}=w600" alt="Artwork created on ${{photo.date}}" loading="lazy" />
          <div class="date-overlay">
            <span class="date-pill">📅 ${{photo.date}}</span>
          </div>
        </div>
      `).join('');

      counterText.textContent = `Showing ${{photosToRender.length}} of ${{allPhotos.length}} artworks`;
    }}

    // Modal Lightbox Functions
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImg');
    const modalCaption = document.getElementById('modalCaption');
    const modalClose = document.getElementById('modalClose');
    const modalPrev = document.getElementById('modalPrev');
    const modalNext = document.getElementById('modalNext');

    function openModal(index) {{
      currentIndex = index;
      const photo = currentPhotos[currentIndex];
      if (!photo) return;
      modalImg.src = `${{photo.baseUrl}}=w1600`;
      modalCaption.innerHTML = `<span style="background:#2563eb; padding:5px 14px; border-radius:9999px;">📅 Created on ${{photo.date}}</span>`;
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
    }}

    function openModalByPhotoId(id) {{
      const idx = currentPhotos.findIndex(p => p.id === id);
      if (idx !== -1) {{
        openModal(idx);
      }} else {{
        const photo = allPhotos.find(p => p.id === id);
        if (photo) {{
          modalImg.src = `${{photo.baseUrl}}=w1600`;
          modalCaption.innerHTML = `<span style="background:#2563eb; padding:5px 14px; border-radius:9999px;">📅 Created on ${{photo.date}}</span>`;
          modal.classList.add('active');
          document.body.style.overflow = 'hidden';
        }}
      }}
    }}

    function closeModal() {{
      modal.classList.remove('active');
      document.body.style.overflow = '';
      modalImg.src = '';
    }}

    modalClose.addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => {{
      if (e.target === modal) closeModal();
    }});

    modalPrev.addEventListener('click', (e) => {{
      e.stopPropagation();
      currentIndex = (currentIndex - 1 + currentPhotos.length) % currentPhotos.length;
      openModal(currentIndex);
    }});

    modalNext.addEventListener('click', (e) => {{
      e.stopPropagation();
      currentIndex = (currentIndex + 1) % currentPhotos.length;
      openModal(currentIndex);
    }});

    // Keyboard Navigation
    window.addEventListener('keydown', (e) => {{
      if (!modal.classList.contains('active')) return;
      if (e.key === 'Escape') closeModal();
      else if (e.key === 'ArrowLeft') {{
        currentIndex = (currentIndex - 1 + currentPhotos.length) % currentPhotos.length;
        openModal(currentIndex);
      }} else if (e.key === 'ArrowRight') {{
        currentIndex = (currentIndex + 1) % currentPhotos.length;
        openModal(currentIndex);
      }}
    }});

    // Initialize
    setupFilters();
    renderReel();
    renderGallery(currentPhotos);
  </script>
</body>
</html>
"""

with open('artwork.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f'Successfully generated artwork.html with all {total_count} photos!')

