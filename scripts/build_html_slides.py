# scripts/build_html_slides.py
"""
High-End Presentation Generator for SHADOW-ML (34 Slides Master Deck)
Produces a bespoke, visually rich, interactive HTML presentation:
- Tailored layouts per slide category (Hero, Danger Grid, 5 Pillars, Pipeline Flow, 
  Agent Cards, Spectral Math, Metric Gauges, Pytest Terminal, Repo Anatomy, Matriks Kriteria Sistem, UI Showcase)
- Dark Chocolate (#0F0804) & Honey Amber (#E8B04A) theme
- Keyboard shortcuts, Speaker Notes drawer (P), Thumbnail drawer (T), Fullscreen (F)
- Zero dollar signs ($), zero raw LaTeX
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "slides.html"

def generate_slides_html() -> str:
    html = """<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SHADOW-ML | Masterclass Presentation (34 Slide Lengkap & Mendalam)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&family=Nunito:wght@600;700;800&family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-primary: #0a0503;
      --bg-secondary: #160b06;
      --bg-card: rgba(38, 21, 11, 0.78);
      --bg-card-hover: rgba(55, 30, 16, 0.9);
      --border-color: rgba(90, 58, 34, 0.7);
      --border-glow: rgba(232, 176, 74, 0.35);
      --text-main: #FFF4E0;
      --text-muted: #d0bba5;
      --text-faint: #8e7a68;
      
      /* Agent Themes */
      --accent-gold: #E8B04A;        /* Honey Amber / General Accent */
      --agent-framer: #F5B83D;       /* Stage 1: Problem Framer */
      --agent-wrangler: #8DB255;     /* Stage 2: Data Wrangler */
      --agent-guardian: #FF5C5C;     /* Stage 3: Model Guardian */
      --agent-storyteller: #D9703F;  /* Stage 4: Insight Storyteller */
      --agent-builder: #5B9BB5;      /* Stage 5: Notebook Builder */
      
      --danger: #FF5C5C;
      --success: #8DB255;
      --info: #5B9BB5;
      --warning: #F5B83D;

      --font-heading: 'Outfit', 'Fredoka', 'Nunito', system-ui, sans-serif;
      --font-body: 'Inter', system-ui, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; -webkit-font-smoothing: antialiased; }

    body {
      background: radial-gradient(ellipse at 50% 30%, #2b160b 0%, #140a05 60%, #070302 100%) !important;
      background-color: #070302 !important;
      color: var(--text-main);
      font-family: var(--font-body);
      overflow: hidden;
      height: 100vh;
      width: 100vw;
      display: flex;
      flex-direction: column;
      position: relative;
    }

    /* Ambient Glows */
    .ambient-glow-1 {
      position: absolute; top: -15%; left: -10%; width: 55vw; height: 55vw;
      background: radial-gradient(circle, rgba(232, 176, 74, 0.12) 0%, rgba(10, 5, 3, 0) 70%);
      pointer-events: none; z-index: 0;
    }
    .ambient-glow-2 {
      position: absolute; bottom: -15%; right: -10%; width: 55vw; height: 55vw;
      background: radial-gradient(circle, rgba(217, 112, 63, 0.1) 0%, rgba(10, 5, 3, 0) 70%);
      pointer-events: none; z-index: 0;
    }
    .ambient-grid {
      position: absolute; inset: 0;
      background-image: linear-gradient(rgba(255, 244, 224, 0.03) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(255, 244, 224, 0.03) 1px, transparent 1px);
      background-size: 40px 40px;
      pointer-events: none; z-index: 0;
    }

    /* Progress Bar */
    .progress-bar-container {
      position: fixed; top: 0; left: 0; width: 100%; height: 4px;
      background: rgba(45, 26, 14, 0.8); z-index: 100;
    }
    .progress-bar {
      height: 100%; width: 3%;
      background: linear-gradient(90deg, #E8B04A, #F5B83D, #8DB255);
      transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1);
      box-shadow: 0 0 10px rgba(232, 176, 74, 0.7);
    }

    /* Header */
    header {
      position: fixed; top: 10px; left: 0; width: 100%; padding: 0 28px;
      display: flex; justify-content: space-between; align-items: center;
      z-index: 50; pointer-events: none;
    }
    .header-logo {
      font-family: var(--font-heading); font-weight: 800; font-size: 1.15rem;
      letter-spacing: 0.5px; color: var(--accent-gold); display: flex; align-items: center; gap: 10px;
      pointer-events: auto;
    }
    .header-logo span {
      font-size: 0.75rem; color: var(--text-muted); font-family: var(--font-body);
      font-weight: 500; background: rgba(232, 176, 74, 0.12); padding: 3px 8px;
      border-radius: 4px; border: 1px solid rgba(232, 176, 74, 0.3);
    }
    .header-controls {
      display: flex; gap: 8px; pointer-events: auto;
    }
    .btn-control {
      background: rgba(38, 21, 11, 0.85); border: 1px solid var(--border-color);
      color: var(--text-main); padding: 5px 12px; border-radius: 6px; font-size: 0.78rem;
      font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 6px;
      transition: all 0.2s ease; backdrop-filter: blur(8px);
    }
    .btn-control:hover {
      background: var(--accent-gold); color: #0a0503; border-color: var(--accent-gold);
      box-shadow: 0 0 12px rgba(232, 176, 74, 0.3);
    }
    .kbd-pill {
      background: rgba(0, 0, 0, 0.4); border: 1px solid rgba(255, 244, 224, 0.2);
      padding: 1px 5px; border-radius: 3px; font-size: 0.68rem; font-family: var(--font-mono);
    }

    /* Deck and Slides */
    main#deck {
      flex: 1; width: 100%; height: 100%; position: relative;
      padding-top: 52px; padding-bottom: 58px;
      display: flex; justify-content: center; align-items: center;
      z-index: 10;
    }
    .slide {
      position: absolute; inset: 52px 28px 58px 28px;
      display: none; flex-direction: column; justify-content: flex-start;
      padding: 16px 24px; opacity: 0; transform: translateY(8px);
      transition: opacity 0.3s ease, transform 0.3s ease;
      overflow-y: auto; overflow-x: hidden;
    }
    .slide.active {
      display: flex; opacity: 1; transform: translateY(0);
    }

    /* Slide Headers */
    .slide-badge {
      display: inline-flex; align-items: center; gap: 6px;
      font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;
      color: var(--accent-gold); background: rgba(232, 176, 74, 0.12);
      border: 1px solid rgba(232, 176, 74, 0.3); padding: 3px 10px; border-radius: 20px;
      margin-bottom: 6px; width: fit-content;
    }
    .slide-title {
      font-family: var(--font-heading); font-size: 2.1rem; font-weight: 800; line-height: 1.18;
      letter-spacing: -0.5px; color: #FFF4E0; margin-bottom: 4px;
    }
    .slide-subtitle {
      font-size: 0.95rem; color: var(--text-muted); margin-bottom: 16px; font-weight: 400;
    }

    /* Common Card Styles */
    .glass-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 16px 20px;
      backdrop-filter: blur(12px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
      transition: border-color 0.2s ease, transform 0.2s ease;
    }
    .glass-card:hover {
      border-color: var(--border-glow);
    }
    .glass-card.highlight {
      border-color: rgba(232, 176, 74, 0.5);
      background: linear-gradient(145deg, rgba(45, 26, 14, 0.85) 0%, rgba(30, 16, 8, 0.92) 100%);
    }

    /* Feature List */
    ul.bullet-list {
      list-style: none; display: flex; flex-direction: column; gap: 10px;
    }
    ul.bullet-list li {
      position: relative; padding-left: 24px; font-size: 0.92rem; line-height: 1.48;
      color: var(--text-main);
    }
    ul.bullet-list li::before {
      content: "◆"; position: absolute; left: 0; top: 0; color: var(--accent-gold);
      font-size: 0.75rem;
    }
    ul.bullet-list li b { color: var(--accent-gold); }

    /* Custom Sleek Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: rgba(10, 5, 3, 0.7); }
    ::-webkit-scrollbar-thumb { background: rgba(232, 176, 74, 0.4); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-gold); }

    /* Code Terminal Container */
    .terminal-box {
      background: #080402; border: 1px solid rgba(90, 58, 34, 0.9);
      border-radius: 10px; overflow: hidden; display: flex; flex-direction: column;
      box-shadow: 0 10px 30px rgba(0,0,0,0.6);
      text-align: left !important;
      width: 100%;
    }
    .terminal-header {
      background: #140a05; padding: 8px 14px; display: flex; align-items: center;
      justify-content: space-between; border-bottom: 1px solid rgba(90, 58, 34, 0.7);
    }
    .terminal-dots { display: flex; gap: 6px; }
    .dot { width: 9px; height: 9px; border-radius: 50%; }
    .dot-red { background: #ff5f56; }
    .dot-yellow { background: #ffbd2e; }
    .dot-green { background: #27c93f; }
    .terminal-title {
      font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-muted);
    }
    .terminal-body {
      padding: 12px 18px; font-family: var(--font-mono); font-size: 0.83rem;
      line-height: 1.55; color: #f8f0e5; text-align: left !important;
      overflow-x: hidden; white-space: pre-wrap; word-break: break-word;
    }
    .terminal-body .c-comment { color: #8e7a68; font-style: italic; }
    .terminal-body .c-keyword { color: #E8B04A; font-weight: 700; }
    .terminal-body .c-func { color: #8DB255; }
    .terminal-body .c-str { color: #D9703F; }
    .terminal-body .c-num { color: #5B9BB5; }
    .terminal-body .c-hl { background: rgba(232, 176, 74, 0.15); border-left: 3px solid #E8B04A; padding-left: 6px; }

    /* Hero Slide Specifics */
    .hero-container {
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      text-align: center; height: 100%; max-width: 1080px; margin: 0 auto;
    }
    .hero-badge-glow {
      display: inline-flex; align-items: center; gap: 8px;
      background: linear-gradient(90deg, rgba(232, 176, 74, 0.15), rgba(217, 112, 63, 0.15));
      border: 1.5px solid rgba(232, 176, 74, 0.5); padding: 6px 18px; border-radius: 30px;
      font-size: 0.85rem; font-weight: 700; color: var(--accent-gold); margin-bottom: 16px;
      box-shadow: 0 0 20px rgba(232, 176, 74, 0.2);
    }
    .hero-h1 {
      font-family: var(--font-heading); font-size: 3.5rem; font-weight: 800; line-height: 1.1;
      margin-bottom: 14px; letter-spacing: -1px;
      background: linear-gradient(135deg, #FFF4E0 30%, #E8B04A 70%, #D9703F 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero-lead {
      font-size: 1.25rem; color: #dfcdb9; max-width: 860px; line-height: 1.5; margin-bottom: 24px;
    }
    .hero-pill-grid {
      display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-bottom: 24px;
    }
    .hero-pill {
      background: rgba(38, 21, 11, 0.85); border: 1px solid rgba(232, 176, 74, 0.3);
      padding: 8px 16px; border-radius: 8px; font-size: 0.85rem; font-weight: 600;
      color: #FFF4E0; display: flex; align-items: center; gap: 8px;
    }
    .hero-meta-footer {
      display: flex; gap: 32px; font-size: 0.85rem; color: var(--text-muted);
      border-top: 1px solid rgba(90, 58, 34, 0.7); padding-top: 16px; width: 100%;
      justify-content: center;
    }
    .hero-meta-footer b { color: var(--accent-gold); }

    /* Layout Grids */
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; height: calc(100% - 90px); }
    .grid-2-wide-left { display: grid; grid-template-columns: 1.25fr 0.75fr; gap: 18px; height: calc(100% - 90px); }
    .grid-2-wide-right { display: grid; grid-template-columns: 0.85fr 1.15fr; gap: 18px; height: calc(100% - 90px); }
    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
    .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
    .grid-5 { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; }

    /* Pillar Cards (Principles & Kriteria Kelayakan) */
    .pillar-card {
      background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px;
      padding: 16px; display: flex; flex-direction: column; gap: 10px; position: relative;
      overflow: hidden;
    }
    .pillar-card::before {
      content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 3px;
      background: var(--accent-gold);
    }
    .pillar-card.agent-1::before { background: var(--agent-framer); }
    .pillar-card.agent-2::before { background: var(--agent-wrangler); }
    .pillar-card.agent-3::before { background: var(--agent-guardian); }
    .pillar-card.agent-4::before { background: var(--agent-storyteller); }
    .pillar-card.agent-5::before { background: var(--agent-builder); }
    .pillar-num {
      font-family: var(--font-heading); font-size: 1.4rem; font-weight: 800;
      color: var(--accent-gold); line-height: 1;
    }
    .pillar-title {
      font-family: var(--font-heading); font-size: 1.05rem; font-weight: 700; color: #FFF4E0;
    }
    .pillar-desc {
      font-size: 0.85rem; color: var(--text-muted); line-height: 1.45;
    }

    /* Warning / Hazard Cards */
    .hazard-card {
      background: rgba(45, 15, 12, 0.75); border: 1px solid rgba(255, 92, 92, 0.4);
      border-radius: 10px; padding: 14px; display: flex; flex-direction: column; gap: 6px;
    }
    .hazard-card:hover { border-color: rgba(255, 92, 92, 0.8); }
    .hazard-icon { font-size: 1.4rem; }
    .hazard-title { font-family: var(--font-heading); font-size: 0.98rem; font-weight: 700; color: #ff8b8b; }
    .hazard-desc { font-size: 0.82rem; color: #f2cfcf; line-height: 1.4; }

    /* Pipeline Flow Chart */
    .pipeline-container {
      display: flex; justify-content: space-between; align-items: stretch;
      gap: 12px; margin: 16px 0; position: relative;
    }
    .pipeline-step {
      flex: 1; background: var(--bg-card); border: 1.5px solid var(--border-color);
      border-radius: 12px; padding: 14px; display: flex; flex-direction: column;
      align-items: center; text-align: center; gap: 8px; position: relative;
      transition: all 0.2s ease;
    }
    .pipeline-step:hover {
      transform: translateY(-4px); box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }
    .pipeline-step.step-1 { border-color: rgba(245, 184, 61, 0.6); }
    .pipeline-step.step-2 { border-color: rgba(141, 178, 85, 0.6); }
    .pipeline-step.step-3 { border-color: rgba(255, 92, 92, 0.6); }
    .pipeline-step.step-4 { border-color: rgba(217, 112, 63, 0.6); }
    .pipeline-step.step-5 { border-color: rgba(91, 155, 181, 0.6); }
    .pipeline-badge {
      font-size: 0.7rem; font-weight: 800; padding: 2px 8px; border-radius: 12px;
      font-family: var(--font-mono);
    }
    .step-1 .pipeline-badge { background: rgba(245, 184, 61, 0.2); color: #F5B83D; }
    .step-2 .pipeline-badge { background: rgba(141, 178, 85, 0.2); color: #8DB255; }
    .step-3 .pipeline-badge { background: rgba(255, 92, 92, 0.2); color: #FF5C5C; }
    .step-4 .pipeline-badge { background: rgba(217, 112, 63, 0.2); color: #D9703F; }
    .step-5 .pipeline-badge { background: rgba(91, 155, 181, 0.2); color: #5B9BB5; }
    .pipeline-title { font-family: var(--font-heading); font-size: 0.95rem; font-weight: 700; color: #FFF; }
    .pipeline-desc { font-size: 0.78rem; color: var(--text-muted); line-height: 1.35; }
    .pipeline-arrow {
      display: flex; align-items: center; justify-content: center;
      color: var(--accent-gold); font-size: 1.2rem; font-weight: bold;
    }

    /* Big Metric Tiles */
    .metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 16px; }
    .metric-tile {
      background: rgba(30, 16, 9, 0.85); border: 1.5px solid var(--border-color);
      border-radius: 12px; padding: 14px; text-align: center; display: flex;
      flex-direction: column; justify-content: center; gap: 4px;
    }
    .metric-tile.highlight { border-color: var(--accent-gold); background: rgba(45, 26, 14, 0.9); }
    .metric-val {
      font-family: var(--font-heading); font-size: 2.2rem; font-weight: 800;
      color: var(--accent-gold); line-height: 1.1;
    }
    .metric-tile.green .metric-val { color: var(--success); }
    .metric-tile.blue .metric-val { color: var(--info); }
    .metric-tile.red .metric-val { color: var(--danger); }
    .metric-label { font-size: 0.78rem; color: var(--text-muted); text-transform: uppercase; font-weight: 600; }
    .metric-sub { font-size: 0.72rem; color: var(--text-faint); font-family: var(--font-mono); }

    /* Confusion Matrix 2x2 Table */
    .matrix-table {
      width: 100%; border-collapse: separate; border-spacing: 4px;
      font-family: var(--font-mono); margin-top: 8px;
    }
    .matrix-table th {
      font-size: 0.75rem; color: var(--text-muted); padding: 4px; text-align: center;
    }
    .matrix-table td {
      padding: 10px; text-align: center; border-radius: 6px; font-weight: 700; font-size: 0.95rem;
    }
    .matrix-cell-tn { background: rgba(141, 178, 85, 0.25); color: #b7e37d; border: 1px solid rgba(141, 178, 85, 0.4); }
    .matrix-cell-fp { background: rgba(255, 92, 92, 0.2); color: #ff9b9b; border: 1px solid rgba(255, 92, 92, 0.3); }
    .matrix-cell-fn { background: rgba(255, 92, 92, 0.2); color: #ff9b9b; border: 1px solid rgba(255, 92, 92, 0.3); }
    .matrix-cell-tp { background: rgba(141, 178, 85, 0.25); color: #b7e37d; border: 1px solid rgba(141, 178, 85, 0.4); }

    /* Mathematical Box */
    .math-card {
      background: rgba(18, 10, 5, 0.95); border: 1px solid rgba(232, 176, 74, 0.4);
      border-radius: 12px; padding: 18px; font-family: var(--font-mono);
      display: flex; flex-direction: column; gap: 12px;
    }
    .math-eq {
      font-size: 1.05rem; color: #FFF4E0; background: rgba(45, 26, 14, 0.6);
      padding: 10px 14px; border-radius: 8px; border-left: 3px solid var(--accent-gold);
    }

    /* Matriks Kriteria Sistem */
    .kriteria-card {
      background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 10px;
      padding: 12px 14px; display: flex; align-items: flex-start; gap: 10px;
    }
    .kriteria-badge {
      font-size: 0.72rem; font-weight: 800; padding: 3px 6px; border-radius: 4px;
      white-space: nowrap; font-family: var(--font-mono);
    }
    .kriteria-badge.pass { background: rgba(141, 178, 85, 0.25); color: #8DB255; border: 1px solid rgba(141, 178, 85, 0.4); }
    .kriteria-badge.ready { background: rgba(232, 176, 74, 0.25); color: #E8B04A; border: 1px solid rgba(232, 176, 74, 0.4); }
    .kriteria-title { font-size: 0.88rem; font-weight: 700; color: #FFF4E0; margin-bottom: 2px; }
    .kriteria-desc { font-size: 0.78rem; color: var(--text-muted); line-height: 1.35; }

    /* Footer Navigation */
    footer {
      position: fixed; bottom: 0; left: 0; width: 100%; height: 50px; padding: 0 28px;
      background: rgba(18, 9, 4, 0.96); border-top: 1px solid rgba(90, 58, 34, 0.8);
      display: flex; justify-content: space-between; align-items: center; z-index: 50;
      backdrop-filter: blur(10px);
    }
    .slide-counter { font-family: var(--font-mono); font-size: 0.82rem; color: var(--text-muted); }
    .slide-counter b { color: var(--accent-gold); }
    .footer-nav { display: flex; align-items: center; gap: 10px; }
    .btn-nav {
      background: rgba(38, 21, 11, 0.9); border: 1px solid var(--border-color); color: #FFF4E0;
      padding: 6px 14px; border-radius: 6px; font-size: 0.82rem; font-weight: 700; cursor: pointer;
      display: flex; align-items: center; gap: 6px; transition: all 0.2s ease;
    }
    .btn-nav:hover:not(:disabled) {
      background: var(--accent-gold); color: #0a0503; border-color: var(--accent-gold);
    }
    .btn-nav:disabled { opacity: 0.3; cursor: not-allowed; }

    /* Speaker Notes Modal */
    #speaker-notes-modal {
      position: fixed; bottom: 58px; left: 28px; right: 28px; max-height: 200px;
      background: rgba(18, 9, 4, 0.97); border: 1.5px solid var(--accent-gold);
      border-radius: 10px; padding: 14px 18px; backdrop-filter: blur(20px); z-index: 90;
      box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.8); display: none; flex-direction: column; overflow-y: auto;
    }
    #speaker-notes-modal.show { display: flex; }
    .notes-header {
      display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;
      border-bottom: 1px solid var(--border-color); padding-bottom: 4px;
    }
    .notes-title {
      font-family: var(--font-heading); font-size: 0.85rem; font-weight: 700; color: var(--accent-gold);
      text-transform: uppercase; letter-spacing: 0.5px;
    }
    .notes-content { font-size: 0.9rem; line-height: 1.55; color: #FFF4E0; }

    /* Thumb Drawer */
    #thumb-drawer {
      position: fixed; top: 0; right: -360px; width: 360px; height: 100%;
      background: rgba(18, 9, 4, 0.98); border-left: 1.5px solid var(--border-color);
      backdrop-filter: blur(20px); z-index: 95; padding: 20px; overflow-y: auto;
      transition: right 0.3s ease; display: flex; flex-direction: column; gap: 8px;
    }
    #thumb-drawer.open { right: 0; }
    .thumb-header {
      font-family: var(--font-heading); font-weight: 700; font-size: 1.05rem;
      color: #FFF4E0; margin-bottom: 10px; display: flex; justify-content: space-between;
      align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 8px;
    }
    .thumb-item {
      padding: 8px 12px; background: rgba(38, 21, 11, 0.7); border: 1px solid var(--border-color);
      border-radius: 6px; cursor: pointer; font-size: 0.78rem; color: #FFF4E0;
      display: flex; align-items: center; gap: 8px; transition: all 0.15s ease;
    }
    .thumb-item:hover, .thumb-item.active {
      background: rgba(232, 176, 74, 0.15); border-color: var(--accent-gold); color: var(--accent-gold);
    }
    .thumb-num {
      font-family: var(--font-mono); font-weight: 700; font-size: 0.72rem; color: var(--accent-gold);
    }

    /* Laser Pointer */
    #laser-pointer {
      position: fixed; width: 14px; height: 14px; border-radius: 50%;
      background: #ff3333;
      box-shadow: 0 0 10px 3px rgba(255, 51, 51, 0.9), 0 0 20px 6px rgba(232, 176, 74, 0.5);
      pointer-events: none; z-index: 9999; display: none;
      transform: translate(-50%, -50%);
    }

    /* Timer Box */
    .timer-box {
      font-family: var(--font-mono); font-size: 0.82rem; color: var(--accent-gold);
      background: rgba(38, 21, 11, 0.9); border: 1px solid var(--border-color);
      padding: 5px 12px; border-radius: 6px; cursor: pointer; user-select: none;
      transition: all 0.2s ease; display: flex; align-items: center; gap: 6px;
    }
    .timer-box:hover {
      border-color: var(--accent-gold); background: rgba(232, 176, 74, 0.15);
    }
    .slide-counter {
      cursor: pointer; user-select: none; transition: color 0.2s ease;
    }
    .slide-counter:hover b {
      text-decoration: underline; color: #FFF;
    }

    /* Print Stylesheet for PDF Export (Ctrl + P) */
    @media print {
      body {
        overflow: visible !important; height: auto !important; width: 100% !important;
        background: #070302 !important; -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }
      header, footer, .progress-bar-container, #speaker-notes-modal, #thumb-drawer,
      .ambient-glow-1, .ambient-glow-2, .ambient-grid, #laser-pointer {
        display: none !important;
      }
      main#deck {
        padding: 0 !important; display: block !important; height: auto !important;
        position: static !important;
      }
      .slide {
        display: flex !important; position: relative !important; inset: auto !important;
        opacity: 1 !important; transform: none !important; page-break-after: always !important;
        break-after: page !important; width: 100vw !important; height: 100vh !important;
        padding: 28px 36px !important; box-sizing: border-box !important; overflow: visible !important;
      }
    }
  </style>
</head>
<body>
  <div id="laser-pointer"></div>
  <div class="ambient-glow-1"></div>
  <div class="ambient-glow-2"></div>
  <div class="ambient-grid"></div>
  <div class="progress-bar-container"><div class="progress-bar" id="progressBar"></div></div>

  <header>
    <div class="header-logo">SHADOW-ML <span>Masterclass & Sidang Dewan Penguji</span></div>
    <div class="header-controls">
      <button class="btn-control" id="btnLaser" title="Laser Pointer (L)">🔴 Laser <span class="kbd-pill">L</span></button>
      <button class="btn-control" id="btnNotesToggle" title="Buka Catatan Pembicara (N / P)">🎙️ Catatan <span class="kbd-pill">N/P</span></button>
      <button class="btn-control" id="btnThumbToggle" title="Daftar Slide (T)">☰ Index <span class="kbd-pill">T</span></button>
      <button class="btn-control" id="btnFullscreen" title="Layar Penuh (F)">⛶ Layar Penuh <span class="kbd-pill">F</span></button>
    </div>
  </header>

  <main id="deck">
"""

    slides_data = get_all_slides_content()
    for s in slides_data:
        html += s

    html += """  </main>

  <div id="speaker-notes-modal">
    <div class="notes-header">
      <div class="notes-title">🎙️ Catatan Lisan Pembicara (Speaker Notes)</div>
      <div style="font-size: 0.75rem; color: var(--text-muted);">Tekan <span class="kbd-pill">N</span> atau <span class="kbd-pill">P</span> untuk menutup</div>
    </div>
    <div class="notes-content" id="notesContentText">Catatan pembicara akan tampil di sini.</div>
  </div>

  <div id="thumb-drawer">
    <div class="thumb-header">
      <span>Daftar 34 Slide Presentasi</span>
      <span style="font-size:0.75rem; color:var(--text-muted); cursor:pointer;" id="btnCloseThumb">✕ Tutup</span>
    </div>
    <div id="thumbList" style="display:flex; flex-direction:column; gap:6px;"></div>
  </div>

  <footer>
    <div class="slide-counter" id="slideCounterBtn" title="Klik untuk melompat ke nomor slide">Slide <b id="currentSlideNum">1</b> dari <span id="totalSlidesNum">34</span></div>
    <div class="timer-box" id="presentationTimer" title="Klik: Jeda/Lanjut | Dobel-klik: Reset">⏱ <span id="timerDisplay">00:00</span></div>
    <div class="footer-nav">
      <button class="btn-nav" id="btnPrev" title="Slide Sebelumnya (Panah Kiri)">◀ Sebelumnya</button>
      <button class="btn-nav" id="btnNext" title="Slide Berikutnya (Panah Kanan / Spasi)">Berikutnya ▶</button>
    </div>
  </footer>

  <script>
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    let currentSlide = 0;

    const progressBar = document.getElementById('progressBar');
    const currentSlideNum = document.getElementById('currentSlideNum');
    const totalSlidesNum = document.getElementById('totalSlidesNum');
    const btnPrev = document.getElementById('btnPrev');
    const btnNext = document.getElementById('btnNext');
    const speakerNotesModal = document.getElementById('speaker-notes-modal');
    const notesContentText = document.getElementById('notesContentText');
    const btnNotesToggle = document.getElementById('btnNotesToggle');
    const thumbDrawer = document.getElementById('thumb-drawer');
    const btnThumbToggle = document.getElementById('btnThumbToggle');
    const btnCloseThumb = document.getElementById('btnCloseThumb');
    const thumbList = document.getElementById('thumbList');
    const btnFullscreen = document.getElementById('btnFullscreen');

    totalSlidesNum.textContent = totalSlides;

    slides.forEach((slide, idx) => {
      const item = document.createElement('div');
      item.className = 'thumb-item';
      const titleElem = slide.querySelector('.slide-title') || slide.querySelector('.hero-h1');
      const title = titleElem ? titleElem.innerText.substring(0, 36) + '...' : ('Slide ' + (idx + 1));
      item.innerHTML = '<span class="thumb-num">#' + (idx + 1) + '</span> <span>' + title + '</span>';
      item.addEventListener('click', () => {
        goToSlide(idx);
        thumbDrawer.classList.remove('open');
      });
      thumbList.appendChild(item);
    });

    function updateSlide() {
      slides.forEach((s, idx) => {
        s.classList.toggle('active', idx === currentSlide);
      });
      currentSlideNum.textContent = currentSlide + 1;
      const progressPercent = ((currentSlide + 1) / totalSlides) * 100;
      progressBar.style.width = progressPercent + '%';

      btnPrev.disabled = currentSlide === 0;
      btnNext.disabled = currentSlide === totalSlides - 1;

      const activeSlide = slides[currentSlide];
      const notesElem = activeSlide.querySelector('.notes-data');
      if (notesElem) {
        notesContentText.innerHTML = notesElem.innerHTML.trim();
      } else {
        notesContentText.innerHTML = "<em>Tidak ada catatan khusus untuk slide ini.</em>";
      }

      const thumbItems = document.querySelectorAll('.thumb-item');
      thumbItems.forEach((t, idx) => {
        t.classList.toggle('active', idx === currentSlide);
      });
    }

    function nextSlide() {
      if (currentSlide < totalSlides - 1) {
        currentSlide++;
        updateSlide();
      }
    }

    function prevSlide() {
      if (currentSlide > 0) {
        currentSlide--;
        updateSlide();
      }
    }

    function goToSlide(idx) {
      if (idx >= 0 && idx < totalSlides) {
        currentSlide = idx;
        updateSlide();
      }
    }

    btnNext.addEventListener('click', nextSlide);
    btnPrev.addEventListener('click', prevSlide);

    btnNotesToggle.addEventListener('click', () => {
      speakerNotesModal.classList.toggle('show');
    });

    btnThumbToggle.addEventListener('click', () => {
      thumbDrawer.classList.toggle('open');
    });

    btnCloseThumb.addEventListener('click', () => {
      thumbDrawer.classList.remove('open');
    });

    btnFullscreen.addEventListener('click', () => {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        document.exitFullscreen().catch(() => {});
      }
    });

    // Timer Presentation Logic
    let timerSeconds = 0;
    let timerRunning = true;
    const timerDisplay = document.getElementById('timerDisplay');
    const presentationTimer = document.getElementById('presentationTimer');
    
    function formatTime(sec) {
      const m = String(Math.floor(sec / 60)).padStart(2, '0');
      const s = String(sec % 60).padStart(2, '0');
      return m + ':' + s;
    }
    
    setInterval(() => {
      if (timerRunning) {
        timerSeconds++;
        timerDisplay.textContent = formatTime(timerSeconds);
      }
    }, 1000);
    
    presentationTimer.addEventListener('click', () => {
      timerRunning = !timerRunning;
      presentationTimer.style.opacity = timerRunning ? '1' : '0.5';
    });
    presentationTimer.addEventListener('dblclick', () => {
      timerSeconds = 0;
      timerDisplay.textContent = '00:00';
    });

    // Virtual Laser Pointer
    let laserActive = false;
    const laserPointer = document.getElementById('laser-pointer');
    const btnLaser = document.getElementById('btnLaser');

    function toggleLaser() {
      laserActive = !laserActive;
      laserPointer.style.display = laserActive ? 'block' : 'none';
      btnLaser.classList.toggle('active', laserActive);
      document.body.style.cursor = laserActive ? 'none' : 'default';
    }

    btnLaser.addEventListener('click', toggleLaser);
    window.addEventListener('mousemove', (e) => {
      if (laserActive) {
        laserPointer.style.left = e.clientX + 'px';
        laserPointer.style.top = e.clientY + 'px';
      }
    });

    // Quick Slide Jump
    const slideCounterBtn = document.getElementById('slideCounterBtn');
    slideCounterBtn.addEventListener('click', () => {
      const target = prompt('Lompat langsung ke slide nomor (1 - ' + totalSlides + '):', currentSlide + 1);
      if (target !== null) {
        const num = parseInt(target, 10);
        if (!isNaN(num) && num >= 1 && num <= totalSlides) {
          goToSlide(num - 1);
        }
      }
    });

    // Touchscreen / Trackpad Swipe Support
    let touchStartX = 0;
    let touchEndX = 0;
    window.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    window.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      if (touchEndX < touchStartX - 60) nextSlide();
      if (touchEndX > touchStartX + 60) prevSlide();
    }, { passive: true });

    // Keyboard Shortcuts
    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {
        e.preventDefault();
        nextSlide();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        prevSlide();
      } else if (e.key === 'Home') {
        e.preventDefault();
        goToSlide(0);
      } else if (e.key === 'End') {
        e.preventDefault();
        goToSlide(totalSlides - 1);
      } else if (e.key === 'p' || e.key === 'P' || e.key === 'n' || e.key === 'N') {
        speakerNotesModal.classList.toggle('show');
      } else if (e.key === 't' || e.key === 'T') {
        thumbDrawer.classList.toggle('open');
      } else if (e.key === 'l' || e.key === 'L') {
        toggleLaser();
      } else if (e.key === 's' || e.key === 'S') {
        timerRunning = !timerRunning;
        presentationTimer.style.opacity = timerRunning ? '1' : '0.5';
      } else if (e.key === 'f' || e.key === 'F') {
        if (!document.fullscreenElement) {
          document.documentElement.requestFullscreen().catch(() => {});
        } else {
          document.exitFullscreen().catch(() => {});
        }
      } else if (e.key === 'Escape') {
        speakerNotesModal.classList.remove('show');
        thumbDrawer.classList.remove('open');
        if (laserActive) toggleLaser();
      }
    });

    updateSlide();
  </script>
</body>
</html>
"""
    return html

def get_all_slides_content() -> list:
    slides = []

    # -------------------------------------------------------------
    # SLIDE 1: HERO SPLASH
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 01: HERO SPLASH -->
    <section class="slide active" data-slide="1">
      <div class="hero-container">
        <div class="hero-badge-glow">⚡ SISTEM MULTI-AGEN TERVALIDASI & SIAP UJI</div>
        <h1 class="hero-h1">SHADOW: Multi-Agent ML Assistant</h1>
        <p class="hero-lead">Sistem Pembelajaran Mesin Multi-Agen Otonom, Transparan, & Bebas Target Leakage Berbasis Blackboard Pattern</p>
        
        <div class="hero-pill-grid">
          <div class="hero-pill">🔒 <b>Bebas Data Leakage:</b> Penapisan Pra-Split 100%</div>
          <div class="hero-pill">⚙️ <b>Python Mengerjakan:</b> Komputasi Deterministik Murni</div>
          <div class="hero-pill">🧪 <b>Pytest Suite:</b> 6/6 Lulus 100% (14.80s)</div>
          <div class="hero-pill">📊 <b>3 Dataset Benchmark:</b> Titanic, Insurance, Telco Churn</div>
        </div>

        <div class="terminal-box" style="max-width: 820px; width: 100%; margin-bottom: 22px;">
          <div class="terminal-header">
            <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="terminal-title">bash — python main.py train &lt;dataset.csv&gt;</div>
          </div>
          <div class="terminal-body"><span class="c-comment"># Eksekusi Otonom Pipeline 5 Agen pada File CSV Apa Pun</span>
<span class="c-keyword">from</span> core.pipeline <span class="c-keyword">import</span> run_pipeline
<span class="c-keyword">from</span> core.llm <span class="c-keyword">import</span> GeminiClient

state = run_pipeline(<span class="c-str">"data/dataset_anda.csv"</span>, client=GeminiClient())
<span class="c-comment"># 5 Agen memproses mandiri -> Terbit: state.json, model.joblib, notebook.ipynb</span></div>
        </div>

        <div class="hero-meta-footer">
          <div>👤 <b>Penyaji:</b> Tim Antigravity</div>
          <div>🎯 <b>Audiens:</b> Dewan Penguji</div>
          <div>📁 <b>Status:</b> Siap Uji & Memenuhi 9/9 Kriteria Kelayakan Sistem</div>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Selamat pagi Bapak dan Ibu Bapak dan Ibu Dewan Penguji. Hari ini kami mempresentasikan SHADOW: Multi-Agent Machine Learning Assistant. Sistem ini dibangun dengan kepatuhan mutlak terhadap standar rekayasa perangkat lunak sains data, memprioritaskan validitas metodologi sains data di atas tampilan kosmetik semata. Seluruh angka berasal dari eksekusi Python lokal, bukan halusinasi LLM.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 2: EXECUTIVE SUMMARY (4 FEATURE CARDS)
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 02: EXECUTIVE SUMMARY -->
    <section class="slide" data-slide="2">
      <div class="slide-badge">RINGKASAN EKSEKUTIF</div>
      <h2 class="slide-title">Integritas Sains Data Berbasis Bukti</h2>
      <p class="slide-subtitle">Menolak rekayasa hasil dan memastikan seluruh angka berasal dari komputasi Scikit-Learn lokal</p>
      
      <div class="grid-2-wide-left">
        <div class="grid-2" style="height: auto; gap: 14px;">
          <div class="glass-card">
            <div style="font-size: 1.5rem; margin-bottom: 6px;">🛡️</div>
            <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: #FFF4E0; margin-bottom: 6px;">Local & Private Execution</h3>
            <p style="font-size: 0.84rem; color: var(--text-muted); line-height: 1.45;">Seluruh pemrosesan dataset mentah, transformasi fitur, dan pelatihan model berjalan 100% lokal pada mesin pengguna tanpa mengunggah data privat ke pihak luar.</p>
          </div>
          <div class="glass-card">
            <div style="font-size: 1.5rem; margin-bottom: 6px;">🎯</div>
            <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: #FFF4E0; margin-bottom: 6px;">Zero Metric Hallucination</h3>
            <p style="font-size: 0.84rem; color: var(--text-muted); line-height: 1.45;">Agen AI dilarang keras mengarang skor metrik, akurasi, atau nilai R2 dari memori generatifnya. Seluruh angka dikunci di state.json oleh Python sebelum narasi dirakit.</p>
          </div>
          <div class="glass-card">
            <div style="font-size: 1.5rem; margin-bottom: 6px;">📜</div>
            <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: #FFF4E0; margin-bottom: 6px;">Forensic Audit Trail</h3>
            <p style="font-size: 0.84rem; color: var(--text-muted); line-height: 1.45;">Setiap keputusan dan komunikasi agen AI dicatat forensik di outputs/llm_log.jsonl lengkap dengan timestamp ISO, nama agen, latensi milidetik, prompt mentah, dan response JSON.</p>
          </div>
          <div class="glass-card">
            <div style="font-size: 1.5rem; margin-bottom: 6px;">🔄</div>
            <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: #FFF4E0; margin-bottom: 6px;">Reproducibility Terjamin</h3>
            <p style="font-size: 0.84rem; color: var(--text-muted); line-height: 1.45;">Setiap sesi riset menghasilkan notebook.ipynb mandiri yang diverifikasi ulang menggunakan nbclient headless kernel python3 tanpa ada runtime error.</p>
          </div>
        </div>

        <div class="terminal-box" style="height: 100%;">
          <div class="terminal-header">
            <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="terminal-title">core/pipeline.py: Penegakan Komputasi Deterministik</div>
          </div>
          <div class="terminal-body"><span class="c-comment"># Evaluasi Python lokal Scikit-Learn</span>
metrics = {
    <span class="c-str">"accuracy"</span>: float(accuracy_score(y_test, y_pred)),
    <span class="c-str">"roc_auc"</span>: float(roc_auc_score(y_test, y_prob)),
    <span class="c-str">"brier_score"</span>: float(brier_score_loss(y_test, y_prob)),
    <span class="c-str">"confusion_matrix"</span>: confusion_matrix(
        y_test, y_pred
    ).tolist()
}

<span class="c-comment"># Metrik dikunci ke state.json SEBELUM agen</span>
<span class="c-comment"># Insight Storyteller diizinkan menulis laporan!</span>
state[<span class="c-str">"evaluation"</span>] = metrics
logger.info(<span class="c-str">"Metrik diverifikasi dari Scikit-Learn."</span>)</div>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Sistem kami membedakan secara tegas antara penalaran agen dan komputasi deterministik. Tidak ada satu pun angka di laporan akhir yang tidak berasal dari eksekusi kode Scikit-Learn lokal. Agen AI hanya bertugas menafsirkan angka yang telah dikomputasi sebelumnya oleh mesin Python.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 3: AUTOML CRISIS (5 HAZARD CARDS)
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 03: AUTOML CRISIS -->
    <section class="slide" data-slide="3">
      <div class="slide-badge" style="color: var(--danger); border-color: rgba(255,92,92,0.4); background: rgba(255,92,92,0.1);">LANDASAN MASALAH</div>
      <h2 class="slide-title">Krisis Integritas pada AutoML & Wrapper LLM Tradisional</h2>
      <p class="slide-subtitle">Lima kegagalan fundamental yang sering merusak validitas sistem machine learning otomatis di industri</p>
      
      <div class="grid-5" style="margin-bottom: 16px;">
        <div class="hazard-card">
          <div class="hazard-icon">⚠️</div>
          <div class="hazard-title">1. Target Leakage</div>
          <div class="hazard-desc">Fitur masa depan atau proksi target bocor ke matriks latih, memicu skor akurasi palsu 99% yang runtuh saat fase produksi.</div>
        </div>
        <div class="hazard-card">
          <div class="hazard-icon">🎭</div>
          <div class="hazard-title">2. Halusinasi Metrik</div>
          <div class="hazard-desc">LLM generatif mengarang angka evaluasi tanpa pernah mengeksekusi interpreter kode Python lokal.</div>
        </div>
        <div class="hazard-card">
          <div class="hazard-icon">💥</div>
          <div class="hazard-title">3. Notebook Rusak</div>
          <div class="hazard-desc">Artefak jupyter kehilangan pustaka dependensi atau urutan sel tidak sinkron sehingga gagal saat direplay.</div>
        </div>
        <div class="hazard-card">
          <div class="hazard-icon">🔄</div>
          <div class="hazard-title">4. Endless Debate</div>
          <div class="hazard-desc">Arsitektur multi-agen berdebat tanpa henti (critique loops), menghabiskan token dan membuat latency membengkak.</div>
        </div>
        <div class="hazard-card">
          <div class="hazard-icon">📦</div>
          <div class="hazard-title">5. Black-Box Decision</div>
          <div class="hazard-desc">Praktisi tidak mengetahui alasan mengapa fitur dibuang atau model dipilih karena tiadanya audit trail.</div>
        </div>
      </div>

      <div class="glass-card" style="border-left: 4px solid var(--danger); display: flex; align-items: center; justify-content: space-between; gap: 16px;">
        <div>
          <div style="font-family: var(--font-heading); font-weight: 700; color: #ff8b8b; font-size: 0.95rem; margin-bottom: 2px;">Contoh Nyata Bahaya Kebocoran Data (Target Leakage):</div>
          <div style="font-size: 0.85rem; color: var(--text-muted);">Pada dataset Churn, kolom <code>NextMonthCharges</code> memiliki korelasi r = 0.999 dengan target. Model naif akan menghasilkan akurasi 100%, padahal data ini belum ada pada t = 0 di dunia nyata! SHADOW menapis fitur ini secara otomatis sebelum partisi train/test dibentuk.</div>
        </div>
        <div style="font-family: var(--font-mono); font-size: 0.8rem; background: rgba(0,0,0,0.5); padding: 8px 14px; border-radius: 6px; white-space: nowrap; border: 1px solid rgba(255,92,92,0.3); color: #ff9b9b;">
          |r| >= 0.90 ➔ AUTO DROP
        </div>
      </div>
      <div class="notes-data" style="display:none;">Banyak sistem AutoML dan wrapper LLM modern gagal di dunia nyata karena lima masalah ini. SHADOW hadir dengan sistem perlindungan deterministik untuk menuntaskan kelima kelemahan tersebut. Kami menolak perdebatan agen tak tentu arah dan memberlakukan penapisan leakage pra-split.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 4: 5 CORE PRINCIPLES (5 PILLAR CARDS)
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 04: 5 PRINCIPLES -->
    <section class="slide" data-slide="4">
      <div class="slide-badge">PONDASI METODOLOGI & ARSITEKTUR</div>
      <h2 class="slide-title">Lima Prinsip Utama yang Mengikat</h2>
      <p class="slide-subtitle">Pondasi arsitektur perangkat lunak yang tidak boleh dilanggar dalam kondisi operasional apa pun</p>
      
      <div class="grid-5" style="margin-bottom: 16px;">
        <div class="pillar-card">
          <div class="pillar-num">I</div>
          <div class="pillar-title">LLM Memutuskan, Python Mengerjakan</div>
          <div class="pillar-desc">Pemisahan mutlak: Agen AI merencanakan strategi dalam format JSON; fungsi Scikit-Learn mengeksekusi komputasi numerik.</div>
        </div>
        <div class="pillar-card">
          <div class="pillar-num">II</div>
          <div class="pillar-title">Semua Angka dari Eksekusi Kode</div>
          <div class="pillar-desc">Setiap angka di laporan akhir (akurasi, ROC-AUC, koefisien) wajib berasal dari kamus fakta Python state.json.</div>
        </div>
        <div class="pillar-card">
          <div class="pillar-num">III</div>
          <div class="pillar-title">Tidak Ada Data Hardcode</div>
          <div class="pillar-desc">Dataset berbeda wajib menghasilkan keputusan, pilihan model, dan grafik yang berbeda sesuai karakteristik intrinsik data.</div>
        </div>
        <div class="pillar-card">
          <div class="pillar-num">IV</div>
          <div class="pillar-title">Gagal Harus Terlihat</div>
          <div class="pillar-desc">Jika koneksi LLM terputus, sistem berhenti seketika dengan pesan transparan. Dilarang menutupi error dengan teks karangan.</div>
        </div>
        <div class="pillar-card">
          <div class="pillar-num">V</div>
          <div class="pillar-title">Klaim Harus Bisa Dibuktikan</div>
          <div class="pillar-desc">Setiap pernyataan performa wajib didukung oleh test case pytest, artefak notebook, dan log eksekusi nyata.</div>
        </div>
      </div>

      <div class="terminal-box">
        <div class="terminal-header">
          <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
          <div class="terminal-title">core/llm.py: Penerapan Prinsip 4 (Gagal Harus Terlihat)</div>
        </div>
        <div class="terminal-body"><span class="c-keyword">try</span>:
    response = client.models.generate_content(model=<span class="c-str">"gemini-3.1-flash-lite"</span>, contents=prompt)
<span class="c-keyword">except</span> Exception <span class="c-keyword">as</span> err:
    <span class="c-comment"># Prinsip Integritas: DILARANG mengarang teks pengganti saat koneksi mati!</span>
    logger.error(f<span class="c-str">"Koneksi LLM terputus: {err}"</span>)
    <span class="c-keyword">raise</span> SystemExit(<span class="c-str">"Pipeline berhenti: Layanan LLM offline (Prinsip Integritas: Gagal Harus Terlihat)."</span>)</div>
      </div>
      <div class="notes-data" style="display:none;">Prinsip ini adalah pakta integritas kami. Kami tidak pernah menutupi kegagalan sistem dengan pesan palsu, dan kami tidak pernah menggunakan data hardcode. Jika dewan penguji mematikan koneksi internet, sistem kami dengan bangga akan menampilkan error transparan dan berhenti dengan aman.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 5: DATA SCOPE & CONTRACT BOUNDARIES
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 05: DATA SCOPE -->
    <section class="slide" data-slide="5">
      <div class="slide-badge">SPESIFIKASI DATA & RUANG LINGKUP</div>
      <h2 class="slide-title">Batasan Data & Cakupan Masalah</h2>
      <p class="slide-subtitle">Spesifikasi masukan dataset tabular mandiri yang didukung secara resmi dan batasan tegas sistem</p>
      
      <div class="grid-2-wide-left">
        <div class="grid-2" style="height: auto; gap: 14px;">
          <div class="glass-card" style="border-left: 4px solid var(--success);">
            <div style="font-family: var(--font-heading); font-size: 1.1rem; color: #b7e37d; margin-bottom: 8px;">🟢 Cakupan Tabular yang Didukung Penuh</div>
            <ul class="bullet-list">
              <li><b>Format Masukan:</b> Satu berkas CSV tabular mandiri (Single CSV file).</li>
              <li><b>Batas Kapasitas:</b> Maksimal ±50.000 baris dan ±50 kolom fitur.</li>
              <li><b>Tipe Fitur:</b> Numerik kontinu/diskrit, kategorikal teks, dan penanda waktu sederhana.</li>
              <li><b>Tipe Tugas:</b> Klasifikasi biner, klasifikasi multikelas, dan regresi nilai kontinu.</li>
              <li><b>Kesiapan Data Uji:</b> Siap diuji langsung pada file CSV baru apa pun dari dewan penguji.</li>
            </ul>
          </div>

          <div class="glass-card" style="border-left: 4px solid var(--danger);">
            <div style="font-family: var(--font-heading); font-size: 1.1rem; color: #ff8b8b; margin-bottom: 8px;">🔴 Batasan Tegas di Luar Ruang Lingkup</div>
            <ul class="bullet-list">
              <li><b>Pemrosesan NLP:</b> Tidak memproses korpus teks bebas besar tanpa struktur.</li>
              <li><b>Computer Vision:</b> Tidak mendukung citra foto, video, atau data spasial 2D/3D.</li>
              <li><b>Sinyal Audio & IoT:</b> Tidak mendukung pemrosesan spektrum suara atau sinyal gelombang.</li>
              <li><b>Grafik Kompleks:</b> Tidak mendukung relasi graph berbobot dinamis.</li>
              <li><b>Multi-Table Relational:</b> Tidak mendukung skema snowflake/star database multi-tabel.</li>
            </ul>
          </div>
        </div>

        <div class="terminal-box" style="height: 100%;">
          <div class="terminal-header">
            <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="terminal-title">core/pipeline.py: Validasi Batasan Masukan Tabular</div>
          </div>
          <div class="terminal-body"><span class="c-keyword">def</span> <span class="c-func">validate_tabular_input</span>(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    
    <span class="c-comment"># Penegakan Batasan Kapasitas Sistem</span>
    <span class="c-keyword">if</span> len(df) > 50_000:
        <span class="c-keyword">raise</span> ValueError(
            <span class="c-str">"Dataset melampaui batas kapasitas sistem (50.000 baris)"</span>
        )
    <span class="c-keyword">if</span> len(df.columns) > 50:
        <span class="c-keyword">raise</span> ValueError(
            <span class="c-str">"Jumlah kolom melampaui batas kapasitas sistem (50 kolom)"</span>
        )
    <span class="c-keyword">if</span> len(df.columns) < 2:
        <span class="c-keyword">raise</span> ValueError(
            <span class="c-str">"Dataset tabular minimal memiliki 2 kolom"</span>
        )
        
    <span class="c-keyword">return</span> df</div>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Batasan data tabular kami terdefinisi dengan sangat jelas. Sistem dirancang fokus dan sangat tangguh, memastikan sistem fokus dan sangat tangguh pada data terstruktur tabular standar industri.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 6: 5-STAGE PIPELINE ARCHITECTURE
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 06: PIPELINE ARCHITECTURE -->
    <section class="slide" data-slide="6">
      <div class="slide-badge">ARSITEKTUR PIPELINE MULTI-AGEN</div>
      <h2 class="slide-title">Arsitektur 5 Tahap Sekuensial Agen</h2>
      <p class="slide-subtitle">Alur linier deterministik berbasis Single State Blackboard (state.json) tanpa perdebatan melingkar</p>
      
      <div class="pipeline-container">
        <div class="pipeline-step step-1">
          <span class="pipeline-badge">TAHAP 1</span>
          <div style="font-size: 1.8rem;">🎯</div>
          <div class="pipeline-title">Problem Framer</div>
          <div class="pipeline-desc">Menentukan sasaran bisnis, identifikasi kolom target, tipe tugas, & seleksi metrik primer (PR-AUC/ROC-AUC/R2).</div>
        </div>
        <div class="pipeline-arrow">➔</div>
        <div class="pipeline-step step-2">
          <span class="pipeline-badge">TAHAP 2</span>
          <div style="font-size: 1.8rem;">🧹</div>
          <div class="pipeline-title">Data Wrangler</div>
          <div class="pipeline-desc">Pemusnahan ID (>95% unik), imputasi median/modus, isolasi leakage pra-split, & perakitan ColumnTransformer.</div>
        </div>
        <div class="pipeline-arrow">➔</div>
        <div class="pipeline-step step-3">
          <span class="pipeline-badge">TAHAP 3</span>
          <div style="font-size: 1.8rem;">⚖️</div>
          <div class="pipeline-title">Model Guardian</div>
          <div class="pipeline-desc">Evaluasi 5-Fold CV: Baseline Dummy vs Model Linear vs Ensemble, overfit check, & penegakan Occam's Razor.</div>
        </div>
        <div class="pipeline-arrow">➔</div>
        <div class="pipeline-step step-4">
          <span class="pipeline-badge">TAHAP 4</span>
          <div style="font-size: 1.8rem;">📊</div>
          <div class="pipeline-title">Insight Storyteller</div>
          <div class="pipeline-desc">Ekstraksi koefisien Scikit-Learn nyata, perenderan 4 diagram PNG publikasi, & wawasan bisnis terverifikasi.</div>
        </div>
        <div class="pipeline-arrow">➔</div>
        <div class="pipeline-step step-5">
          <span class="pipeline-badge">TAHAP 5</span>
          <div style="font-size: 1.8rem;">📓</div>
          <div class="pipeline-title">Notebook Builder</div>
          <div class="pipeline-desc">Sintesis notebook.ipynb mandiri, validasi re-eksekusi headless nbclient, & ekspor model.joblib + schema.json.</div>
        </div>
      </div>

      <div class="glass-card" style="display: flex; align-items: center; justify-content: space-between; gap: 20px;">
        <div>
          <div style="font-family: var(--font-heading); font-weight: 700; color: var(--accent-gold); font-size: 0.95rem; margin-bottom: 2px;">Blackboard Pattern: Single Source of Truth (SSOT)</div>
          <div style="font-size: 0.85rem; color: var(--text-muted);">Setiap agen membaca <code>state.json</code>, menambahkan hasil kerjanya, lalu menyerahkan kendali ke tahap berikutnya secara sekuensial. Tidak ada agen yang berbicara mundur atau saling mendebat. Ini menjamin latensi rendah, determinisme mutlak, dan keandalan tinggi.</div>
        </div>
        <div style="font-family: var(--font-mono); font-size: 0.78rem; background: rgba(0,0,0,0.6); padding: 10px 16px; border-radius: 8px; border: 1px solid var(--border-color); white-space: nowrap; color: #b7e37d;">
          outputs/&lt;run_id&gt;/state.json
        </div>
      </div>
      <div class="notes-data" style="display:none;">Arsitektur kami melarang keras perdebatan berulang antar-agen (critique loops). Alur kami berjalan maju sekuensial. Setiap agen membaca SharedState, menambahkan hasil kerjanya, lalu menyerahkan kendali ke tahap berikutnya. Tidak ada loop yang bisa membuat sistem terjebak.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 7: LLM DISCIPLINE & FORENSIC AUDIT TRAIL
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 07: LLM DISCIPLINE -->
    <section class="slide" data-slide="7">
      <div class="slide-badge">MANAJEMEN LLM & KEAMANAN</div>
      <h2 class="slide-title">Disiplin LLM & Audit Trail Forensik</h2>
      <p class="slide-subtitle">Penyedia tunggal Gemini, isolasi API key lokal, skema JSON ketat, dan perekaman transparan llm_log.jsonl</p>
      
      <div class="grid-2">
        <div class="glass-card" style="display: flex; flex-direction: column; justify-content: space-around;">
          <div>
            <h3 style="font-family: var(--font-heading); font-size: 1.1rem; color: var(--accent-gold); margin-bottom: 8px;">Pilar Pengendalian LLM:</h3>
            <ul class="bullet-list">
              <li><b>Penyedia Tunggal:</b> Menggunakan model Gemini via gateway terpusat di <code>core/llm.py</code>.</li>
              <li><b>Keamanan Kredensial:</b> API key disimpan di berkas <code>.env</code> lokal (dilengkapi template <code>.env.example</code>).</li>
              <li><b>Validasi Skema JSON:</b> Respons LLM diwajibkan berupa JSON terstruktur. Format cacat memicu retry otomatis maksimal 2 kali.</li>
              <li><b>Perekaman Forensik:</b> Setiap permintaan dicatat di <code>outputs/&lt;run_id&gt;/llm_log.jsonl</code>.</li>
            </ul>
          </div>
          <div style="background: rgba(45, 26, 14, 0.6); border: 1px solid var(--border-color); padding: 12px; border-radius: 8px;">
            <div style="font-size: 0.82rem; color: var(--text-muted);"><b style="color:var(--accent-gold);">Bukti Nyata Panggilan API:</b> Log forensik membuktikan kepada dewan penguji bahwa agen AI kami benar-benar memanggil LLM secara riil, bukan sekadar simulasi teks atau fungsi tiruan.</div>
          </div>
        </div>

        <div class="terminal-box">
          <div class="terminal-header">
            <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="terminal-title">outputs/run_titanic/llm_log.jsonl (Audit Trail Nyata)</div>
          </div>
          <div class="terminal-body">{
  <span class="c-keyword">"timestamp"</span>: <span class="c-str">"2026-10-18T07:15:22.104Z"</span>,
  <span class="c-keyword">"agent"</span>: <span class="c-str">"problem_framer"</span>,
  <span class="c-keyword">"model"</span>: <span class="c-str">"gemini-3.1-flash-lite"</span>,
  <span class="c-keyword">"latency_ms"</span>: <span class="c-num">1240</span>,
  <span class="c-keyword">"prompt"</span>: <span class="c-str">"Analisis ringkasan statistik dataset..."</span>,
  <span class="c-keyword">"response"</span>: {
    <span class="c-keyword">"problem_statement"</span>: <span class="c-str">"Prediksi kelangsungan hidup penumpang"</span>,
    <span class="c-keyword">"target_column"</span>: <span class="c-str">"Survived"</span>,
    <span class="c-keyword">"task_type"</span>: <span class="c-str">"binary_classification"</span>,
    <span class="c-keyword">"primary_metric"</span>: <span class="c-str">"pr_auc"</span>
  }
}</div>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Pencatatan llm_log.jsonl membuktikan kepada penguji bahwa agen AI kami benar-benar memanggil LLM secara nyata dan menghasilkan keputusan terstruktur. Setiap panggilan memiliki timestamp dan catatan latensi yang dapat diaudit kapan saja.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 8: STAGE 1 - PROBLEM FRAMER
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 08: PROBLEM FRAMER -->
    <section class="slide" data-slide="8">
      <div class="slide-badge" style="color: var(--agent-framer); border-color: rgba(245,184,61,0.4); background: rgba(245,184,61,0.1);">TAHAP 1: PROBLEM FRAMER</div>
      <h2 class="slide-title">Perumusan Masalah & Seleksi Metrik Primer</h2>
      <p class="slide-subtitle">Menganalisis distribusi target dan menetapkan kriteria evaluasi matematis yang objektif</p>
      
      <div class="grid-2">
        <div class="glass-card">
          <h3 style="font-family: var(--font-heading); font-size: 1.15rem; color: var(--agent-framer); margin-bottom: 12px;">Kemampuan Analisis Tahap 1:</h3>
          <ul class="bullet-list">
            <li><b>Deteksi Tipe Tugas Otomatis:</b> Mengklasifikasikan biner (2 kelas unik), multikelas (3-20 kelas unik), atau regresi kontinu berbasis kardinalitas kolom target.</li>
            <li><b>Seleksi Metrik Matematis Skeptis:</b> Mengutamakan PR-AUC dan ROC-AUC jika kelas minoritas timpang (imbalance > 70:30), serta R2 untuk regresi.</li>
            <li><b>Koreksi Akurasi Mentah:</b> Menolak akurasi mentah pada dataset tidak seimbang untuk mencegah ilusi performa tinggi.</li>
            <li><b>Validasi Deterministik Python:</b> Python memverifikasi secara ketat bahwa kolom target yang ditunjuk LLM benar-benar eksis di CSV.</li>
          </ul>
        </div>

        <div class="terminal-box">
          <div class="terminal-header">
            <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="terminal-title">core/prompts/framer.py: Kontrak Skema JSON</div>
          </div>
          <div class="terminal-body"><span class="c-comment"># Template Prompt Terstruktur Problem Framer</span>
FRAMER_PROMPT_TEMPLATE = <span class="c-str">\"\"\"
Analisis ringkasan statistik dataset berikut:
{stats_summary}

Kembalikan jawaban HANYA dalam format JSON valid:
{
  "problem_statement": "&lt;deskripsi sasaran bisnis&gt;",
  "target_column": "&lt;nama kolom target tepat&gt;",
  "task_type": "binary_classification" | "multiclass" | "regression",
  "primary_metric": "roc_auc" | "pr_auc" | "r2" | "rmse"
}
\"\"\"</span></div>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Tahap 1 mencegah kesalahan paling umum pada data science: salah memilih metrik evaluasi. Problem Framer memastikan metrik yang dipilih benar-benar mencerminkan tujuan bisnis, terutama saat menghadapi data dengan ketimpangan kelas yang parah.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 9: CODE STAGE 1 IMPLEMENTATION
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 09: CODE STAGE 1 -->
    <section class="slide" data-slide="9">
      <div class="slide-badge" style="color: var(--agent-framer); border-color: rgba(245,184,61,0.4); background: rgba(245,184,61,0.1);">KODE IMPLEMENTASI TAHAP 1</div>
      <h2 class="slide-title">Implementasi Logika Problem Framer</h2>
      <p class="slide-subtitle">Potongan kode asli orkestrasi perumusan masalah dan penegakan target deterministik di core/pipeline.py</p>
      
      <div class="grid-2-wide-left">
        <div class="terminal-box">
          <div class="terminal-header">
            <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="terminal-title">core/pipeline.py: run_stage_framing</div>
          </div>
          <div class="terminal-body"><span class="c-keyword">def</span> <span class="c-func">run_stage_framing</span>(df: pd.DataFrame, state: SharedState, client: GeminiClient):
    stats_summary = profile_dataset_basic(df)
    prompt = build_framing_prompt(stats_summary)
    
    <span class="c-comment"># Panggilan LLM dengan validasi JSON otomatis</span>
    response = client.call_structured_json(
        agent_name=<span class="c-str">"Problem Framer"</span>, prompt=prompt
    )
    
    <span class="c-comment"># Validasi Deterministik Python (Anti-Halusinasi)</span>
    target_col = response[<span class="c-str">"target_column"</span>]
    <span class="c-hl"><span class="c-keyword">if</span> target_col <span class="c-keyword">not in</span> df.columns:</span>
    <span class="c-hl">    <span class="c-keyword">raise</span> ValueError(f<span class="c-str">"Target '{target_col}' tidak ada di CSV!"</span>)</span>
        
    state.framing = {
        <span class="c-str">"problem_statement"</span>: response[<span class="c-str">"problem_statement"</span>],
        <span class="c-str">"target_column"</span>: target_col,
        <span class="c-str">"task_type"</span>: response[<span class="c-str">"task_type"</span>],
        <span class="c-str">"primary_metric"</span>: response[<span class="c-str">"primary_metric"</span>]
    }
    <span class="c-keyword">return</span> state.framing</div>
        </div>

        <div class="glass-card" style="display: flex; flex-direction: column; justify-content: center; gap: 14px;">
          <h3 style="font-family: var(--font-heading); font-size: 1.1rem; color: var(--agent-framer);">Jaminan Fail-Fast Python:</h3>
          <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.5;">Perhatikan baris validasi Python yang disorot:</p>
          <div style="background: rgba(0,0,0,0.5); padding: 12px; border-radius: 8px; font-family: var(--font-mono); font-size: 0.8rem; border-left: 3px solid var(--danger); color: #ff9b9b;">
            if target_col not in df.columns:<br>&nbsp;&nbsp;&nbsp;&nbsp;raise ValueError(...)
          </div>
          <p style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.5;">Jika LLM berhalusinasi dan menunjuk nama kolom fiktif, eksekusi Python langsung membatalkan operasi seketika. Keputusan keliru agen tidak akan pernah lolos ke tahap pembersihan data.</p>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Perhatikan baris validasi Python: jika LLM mengalami halusinasi dan menunjuk kolom fiktif, Python langsung membatalkan eksekusi dengan pesan kesalahan yang jelas. Ini bukti nyata penerapan prinsip 'LLM Memutuskan, Python Mengerjakan'.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 10: STAGE 2 - DATA WRANGLER
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 10: DATA WRANGLER -->
    <section class="slide" data-slide="10">
      <div class="slide-badge" style="color: var(--agent-wrangler); border-color: rgba(141,178,85,0.4); background: rgba(141,178,85,0.1);">TAHAP 2: DATA WRANGLER</div>
      <h2 class="slide-title">Pembersihan Data Higienis & Fit-in-Fold</h2>
      <p class="slide-subtitle">Menolak pembersihan kotor di awal dan membungkus transformasi di Scikit-Learn ColumnTransformer</p>
      
      <div class="grid-4" style="margin-bottom: 16px;">
        <div class="glass-card">
          <div style="font-size: 1.5rem; margin-bottom: 6px;">🗑️</div>
          <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: #b7e37d; margin-bottom: 4px;">Pemusnahan ID</h3>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.4;">Kolom teks dengan rasio keunikan > 95% (PassengerId, customerID) otomatis didrop karena tidak memiliki daya prediksi.</p>
        </div>
        <div class="glass-card">
          <div style="font-size: 1.5rem; margin-bottom: 6px;">📊</div>
          <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: #b7e37d; margin-bottom: 4px;">Imputasi Median & Modus</h3>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.4;">Menggunakan median untuk fitur numerik agar kebal terhadap pencilan (outlier), dan modus untuk data kategorikal.</p>
        </div>
        <div class="glass-card">
          <div style="font-size: 1.5rem; margin-bottom: 6px;">🏷️</div>
          <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: #b7e37d; margin-bottom: 4px;">One-Hot Encoding</h3>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.4;">Menetapkan handle_unknown='ignore' dan drop='first' untuk mencegah Dummy Variable Trap dan crash saat inferensi.</p>
        </div>
        <div class="glass-card">
          <div style="font-size: 1.5rem; margin-bottom: 6px;">🔒</div>
          <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: #b7e37d; margin-bottom: 4px;">Fit-in-Fold Strictness</h3>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.4;">Parameter scaling dan imputasi HANYA dihitung pada data latih fold aktif. Nol kebocoran distribusi ke data uji!</p>
        </div>
      </div>

      <div class="terminal-box">
        <div class="terminal-header">
          <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
          <div class="terminal-title">core/tools/cleaning.py: Identifikasi & Drop Identifier (>95% Unik)</div>
        </div>
        <div class="terminal-body"><span class="c-keyword">def</span> <span class="c-func">clean_high_cardinality_identifiers</span>(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    drop_cols, n_rows = [], len(df)
    <span class="c-keyword">for</span> col <span class="c-keyword">in</span> df.columns:
        <span class="c-keyword">if</span> df[col].dtype == <span class="c-str">"object"</span> <span class="c-keyword">and</span> (df[col].nunique() / n_rows) > <span class="c-num">0.95</span>:
            drop_cols.append(col)
    <span class="c-keyword">return</span> df.drop(columns=drop_cols), drop_cols</div>
      </div>
      <div class="notes-data" style="display:none;">Banyak praktisi ML melakukan kesalahan fatal dengan mengisi missing values di seluruh CSV sebelum split train/test. Data Wrangler kami menjamin 100% bebas dari kebocoran distribusi dengan membungkus seluruh tahapan ke dalam Scikit-Learn Pipeline resmi.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 11: CODE STAGE 2 - COLUMNTRANSFORMER
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 11: CODE STAGE 2 -->
    <section class="slide" data-slide="11">
      <div class="slide-badge" style="color: var(--agent-wrangler); border-color: rgba(141,178,85,0.4); background: rgba(141,178,85,0.1);">KODE IMPLEMENTASI TAHAP 2</div>
      <h2 class="slide-title">Pipeline Scikit-Learn Fit-in-Fold</h2>
      <p class="slide-subtitle">Perakitan ColumnTransformer modular untuk menjamin reproduktibilitas produksi di core/tools/cleaning.py</p>
      
      <div class="grid-2-wide-left">
        <div class="terminal-box">
          <div class="terminal-header">
            <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="terminal-title">core/tools/cleaning.py: build_preprocessor_pipeline</div>
          </div>
          <div class="terminal-body"><span class="c-keyword">def</span> <span class="c-func">build_preprocessor_pipeline</span>(num_cols: List[str], cat_cols: List[str]) -> ColumnTransformer:
    numeric_transformer = Pipeline(steps=[
        (<span class="c-str">'imputer'</span>, SimpleImputer(strategy=<span class="c-str">'median'</span>)),
        (<span class="c-str">'scaler'</span>, StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        (<span class="c-str">'imputer'</span>, SimpleImputer(strategy=<span class="c-str">'most_frequent'</span>)),
        (<span class="c-str">'onehot'</span>, OneHotEncoder(handle_unknown=<span class="c-str">'ignore'</span>, drop=<span class="c-str">'first'</span>))
    ])
    
    preprocessor = ColumnTransformer(transformers=[
        (<span class="c-str">'num'</span>, numeric_transformer, num_cols),
        (<span class="c-str">'cat'</span>, categorical_transformer, cat_cols)
    ])
    <span class="c-keyword">return</span> preprocessor</div>
        </div>

        <div class="glass-card" style="display: flex; flex-direction: column; justify-content: center; gap: 12px;">
          <h3 style="font-family: var(--font-heading); font-size: 1.1rem; color: var(--agent-wrangler);">Keunggulan Arsitektur Preprocessor:</h3>
          <ul class="bullet-list">
            <li><b>Pemisahan Jalur Mandiri:</b> Jalur numerik dan kategorikal berjalan independen tanpa saling mencemari tipe data.</li>
            <li><b>Pencegahan Dummy Variable Trap:</b> Parameter <code>drop='first'</code> mengeliminasi kolinearitas sempurna pada data kategori biner.</li>
            <li><b>Tahan Kategori Baru:</b> Parameter <code>handle_unknown='ignore'</code> memastikan model tidak melempar error saat inferensi data baru.</li>
            <li><b>Export Ready:</b> Objek preprocessor siap diserialisasikan ke dalam berkas <code>model.joblib</code>.</li>
          </ul>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Penggunaan drop='first' pada OneHotEncoder mencegah terjadinya Dummy Variable Trap (multikolinearitas sempurna). Parameter handle_unknown='ignore' menjamin model tidak crash jika bertemu kategori baru saat fase produksi nanti.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 12: TARGET LEAKAGE DETECTION ALGORITHM
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 12: LEAKAGE DETECTION -->
    <section class="slide" data-slide="12">
      <div class="slide-badge" style="color: var(--danger); border-color: rgba(255,92,92,0.4); background: rgba(255,92,92,0.1);">DETEKSI DATA LEAKAGE</div>
      <h2 class="slide-title">Algoritma Penapisan Kebocoran Target</h2>
      <p class="slide-subtitle">Mengisolasi dan memusnahkan fitur proksi masa depan sebelum matriks pelatihan dibentuk</p>
      
      <div class="grid-3" style="margin-bottom: 16px;">
        <div class="glass-card" style="border-top: 3px solid var(--danger);">
          <div style="font-family: var(--font-heading); font-size: 1.05rem; color: #ff8b8b; margin-bottom: 6px;">1. Ambang Batas Korelasi</div>
          <p style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.45;">Fitur numerik dengan korelasi absolut Pearson <b>|r| >= 0.90</b> terhadap target langsung ditandai sebagai indikator kebocoran masa depan.</p>
        </div>
        <div class="glass-card" style="border-top: 3px solid var(--danger);">
          <div style="font-family: var(--font-heading); font-size: 1.05rem; color: #ff8b8b; margin-bottom: 6px;">2. Rasio Kardinalitas 1:1</div>
          <p style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.45;">Kolom dengan pemetaan nilai unik 1 banding 1 terhadap target otomatis diisolasi untuk mencegah penghafalan ID target.</p>
        </div>
        <div class="glass-card" style="border-top: 3px solid var(--danger);">
          <div style="font-family: var(--font-heading); font-size: 1.05rem; color: #ff8b8b; margin-bottom: 6px;">3. Eliminasi Pra-Split</div>
          <p style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.45;">Seluruh fitur bocor dihapus secara permanen dari dataset SEBELUM pembagian train/test dilakukan. Nol toleransi kebocoran!</p>
        </div>
      </div>

      <div class="glass-card" style="display: flex; align-items: center; justify-content: space-between; border-left: 4px solid var(--success);">
        <div>
          <div style="font-family: var(--font-heading); font-weight: 700; color: #b7e37d; font-size: 0.95rem; margin-bottom: 2px;">Bukti Pengujian Pytest: test_planted_leakage_is_detected</div>
          <div style="font-size: 0.85rem; color: var(--text-muted);">Pada suite pengujian otomatis, kami sengaja menyuntikkan kolom bocor buatan ke dataset. Sistem SHADOW terbukti mendeteksi dan mengeliminasi kolom tersebut 100% tanpa campur tangan manusia.</div>
        </div>
        <div style="font-family: var(--font-mono); font-size: 0.82rem; background: rgba(141,178,85,0.2); color: #8DB255; padding: 6px 12px; border-radius: 6px; border: 1px solid rgba(141,178,85,0.4); white-space: nowrap;">
          PASSED [ 33% ]
        </div>
      </div>
      <div class="notes-data" style="display:none;">Jika ada kolom yang memiliki korelasi 0.99 dengan target, model biasa akan terlihat sangat pintar padahal ia hanya menghafal jawaban masa depan. Algoritma kami membuang fitur tersebut sebelum model sempat melihatnya. Ini diverifikasi di test_planted_leakage_is_detected.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 13: CODE LEAKAGE PROFILING
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 13: CODE LEAKAGE PROFILING -->
    <section class="slide" data-slide="13">
      <div class="slide-badge" style="color: var(--danger); border-color: rgba(255,92,92,0.4); background: rgba(255,92,92,0.1);">KODE DETEKSI LEAKAGE</div>
      <h2 class="slide-title">Logika Deteksi Leakage di Profiling</h2>
      <p class="slide-subtitle">Potongan kode asli penapisan korelasi dan kardinalitas di core/tools/profiling.py</p>
      
      <div class="grid-2-wide-left">
        <div class="terminal-box">
          <div class="terminal-header">
            <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="terminal-title">core/tools/profiling.py: detect_target_leakage</div>
          </div>
          <div class="terminal-body"><span class="c-keyword">def</span> <span class="c-func">detect_target_leakage</span>(df: pd.DataFrame, target_col: str, threshold: float = <span class="c-num">0.90</span>) -> List[str]:
    leakage_cols = []
    y = df[target_col]
    
    <span class="c-keyword">for</span> col <span class="c-keyword">in</span> df.columns:
        <span class="c-keyword">if</span> col == target_col:
            <span class="c-keyword">continue</span>
            
        <span class="c-comment"># 1. Cek rasio keunikan identik (1:1 mapping)</span>
        <span class="c-keyword">if</span> df[col].nunique() == y.nunique() <span class="c-keyword">and</span> (df[col].values == y.values).all():
            leakage_cols.append(col)
            <span class="c-keyword">continue</span>
            
        <span class="c-comment"># 2. Cek korelasi numerik absolut</span>
        <span class="c-keyword">if</span> pd.api.types.is_numeric_dtype(df[col]) <span class="c-keyword">and</span> pd.api.types.is_numeric_dtype(y):
            corr = abs(df[col].corr(y))
            <span class="c-keyword">if</span> corr >= threshold:
                leakage_cols.append(col)
                
    <span class="c-keyword">return</span> leakage_cols</div>
        </div>

        <div class="glass-card" style="display: flex; flex-direction: column; justify-content: center; gap: 12px;">
          <h3 style="font-family: var(--font-heading); font-size: 1.1rem; color: #ff8b8b;">Analisis Komputasi Murni:</h3>
          <ul class="bullet-list">
            <li><b>NumPy & Pandas Murni:</b> Perhitungan korelasi dihitung langsung oleh pustaka numerik tanpa keterlibatan prompt LLM.</li>
            <li><b>Penanganan Nilai Absolut:</b> Menggunakan <code>abs(corr)</code> untuk menangkap kebocoran baik berarah positif maupun berkorelasi terbalik (invers).</li>
            <li><b>Otomasi Eliminasi:</b> Daftar <code>leakage_cols</code> langsung dikunci ke dalam <code>state.data_cleaning['dropped_columns']</code>.</li>
          </ul>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Fungsi ini dieksekusi oleh Python sebelum Data Wrangler mulai bekerja. Fitur bocor langsung dieliminasi dari state.json sehingga model terhindar dari overfitting fatal.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 14: SPECTRAL MATH: GRAM MATRIX & RIDGE L2
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 14: SPECTRAL MATH -->
    <section class="slide" data-slide="14">
      <div class="slide-badge" style="color: var(--accent-gold); border-color: rgba(232,176,74,0.4); background: rgba(232,176,74,0.1);">PEMBEDAHAN MATEMATIKA SPEKTRAL</div>
      <h2 class="slide-title">Matriks Gram, Multikolinearitas, & Solusi Ridge L2</h2>
      <p class="slide-subtitle">Bukti komputasional spektakuler dari scripts/demo_gram_matrix_vif.py mengenai stabilitas aljabar linier</p>
      
      <div class="grid-2" style="margin-bottom: 14px;">
        <div class="math-card" style="border-color: rgba(255,92,92,0.5);">
          <div style="font-family: var(--font-heading); font-size: 1.1rem; color: #ff8b8b; font-weight: 700;">💥 Keruntuhan OLS Biasa (Ill-Conditioned)</div>
          <div class="math-eq">beta = (X^T * X)^(-1) * X^T * y</div>
          <ul class="bullet-list" style="font-family: var(--font-body); font-size: 0.85rem;">
            <li>Jika fitur kolinear: det(X^T * X) mendekati 0, lambda_min -> 0</li>
            <li><b>Condition Number Meledak:</b> <span style="color:#ff8b8b; font-weight:700;">23,791,694.1</span> (Jauh melampaui batas aman 30)</li>
            <li><b>Variansi Koefisien OLS:</b> <span style="color:#ff8b8b; font-weight:700;">45,266.69</span> (Ledakan varians liar!)</li>
            <li><b>Nilai VIF Fitur Kolinear:</b> <span style="color:#ff8b8b; font-weight:700;">3,695,678.8</span></li>
          </ul>
        </div>

        <div class="math-card" style="border-color: rgba(141,178,85,0.5);">
          <div style="font-family: var(--font-heading); font-size: 1.1rem; color: #b7e37d; font-weight: 700;">✅ Penyelamatan Ridge L2 (Regularized)</div>
          <div class="math-eq">beta_ridge = (X^T * X + lambda * I)^(-1) * X^T * y</div>
          <ul class="bullet-list" style="font-family: var(--font-body); font-size: 0.85rem;">
            <li>Penalti diagonal: lambda_new = lambda_old + lambda_penalti</li>
            <li><b>Condition Number Terkoreksi:</b> <span style="color:#b7e37d; font-weight:700;">421.5</span> (Turun drastis jutaan kali lipat!)</li>
            <li><b>Variansi Estimator Ridge:</b> <span style="color:#b7e37d; font-weight:700;">0.8005</span> (Sangat stabil & teratur)</li>
            <li><b>Estimator Kokoh:</b> Menghilangkan sensibilitas terhadap gangguan derau data</li>
          </ul>
        </div>
      </div>

      <div class="glass-card" style="display: flex; align-items: center; justify-content: space-between;">
        <div style="font-size: 0.85rem; color: var(--text-muted);">
          <b>Kesimpulan Ilmiah:</b> Model linier tanpa regularisasi runtuh seketika saat berhadapan dengan data kolinear. Inilah mengapa SHADOW menetapkan <code>Ridge(alpha=1.0)</code> dan <code>LogisticRegression(penalty='l2')</code> sebagai standar baku model champion.
        </div>
      </div>
      <div class="notes-data" style="display:none;">Inilah pembuktian matematis tingkat tinggi kami. Kami mendemonstrasikan bagaimana korelasi tinggi membuat matriks Gram X transpose X menjadi singular. Penalti L2 menyelamatkan model dengan menambahkan lambda pada diagonal matriks, menekan condition number dari 23.7 juta menjadi 421.5.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 15: CODE SPECTRAL MATH DEMO
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 15: CODE SPECTRAL MATH DEMO -->
    <section class="slide" data-slide="15">
      <div class="slide-badge" style="color: var(--accent-gold); border-color: rgba(232,176,74,0.4); background: rgba(232,176,74,0.1);">KODE PEMBUKTIAN MATEMATIKA</div>
      <h2 class="slide-title">Demonstrasi Spektral Matriks Gram & VIF</h2>
      <p class="slide-subtitle">Potongan kode eksekusi nyata dari scripts/demo_gram_matrix_vif.py dengan hasil numerik riil</p>
      
      <div class="grid-2-wide-left">
        <div class="terminal-box">
          <div class="terminal-header">
            <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="terminal-title">scripts/demo_gram_matrix_vif.py</div>
          </div>
          <div class="terminal-body"><span class="c-keyword">import</span> numpy <span class="c-keyword">as</span> np

<span class="c-comment"># 1. Hitung Matriks Gram X^T * X & Nilai Eigen</span>
gram_matrix = X.T @ X
eigenvals = np.linalg.eigvals(gram_matrix)
cond_orig = np.max(eigenvals) / np.min(eigenvals)

<span class="c-comment"># Output Asli: Condition Number = 23,791,694.1 (Singular!)</span>
<span class="c-comment"># Variansi Estimator OLS = 45,266.69</span>

<span class="c-comment"># 2. Penyelamatan Spektral via Penalti Ridge L2 (lambda = 1.0)</span>
gram_ridge = gram_matrix + <span class="c-num">1.0</span> * np.eye(gram_matrix.shape[<span class="c-num">0</span>])
ridge_eigenvals = np.linalg.eigvals(gram_ridge)
cond_ridge = np.max(ridge_eigenvals) / np.min(ridge_eigenvals)

<span class="c-comment"># Output Ridge L2: Condition Number = 421.5</span>
<span class="c-comment"># Variansi Estimator Ridge = 0.8005 (Stabil!)</span></div>
        </div>

        <div class="glass-card" style="display: flex; flex-direction: column; justify-content: center; gap: 14px;">
          <h3 style="font-family: var(--font-heading); font-size: 1.1rem; color: var(--accent-gold);">Rangkuman Bukti Empiris:</h3>
          <div style="background: rgba(0,0,0,0.4); padding: 10px; border-radius: 8px; border: 1px solid var(--border-color);">
            <div style="font-size: 0.78rem; color: var(--text-muted); text-transform: uppercase;">Condition Number OLS:</div>
            <div style="font-family: var(--font-mono); font-size: 1.25rem; font-weight: 700; color: #ff8b8b;">23,791,694.1</div>
          </div>
          <div style="background: rgba(0,0,0,0.4); padding: 10px; border-radius: 8px; border: 1px solid var(--border-color);">
            <div style="font-size: 0.78rem; color: var(--text-muted); text-transform: uppercase;">Condition Number Ridge L2:</div>
            <div style="font-family: var(--font-mono); font-size: 1.25rem; font-weight: 700; color: #b7e37d;">421.5</div>
          </div>
          <p style="font-size: 0.84rem; color: var(--text-muted); line-height: 1.45;">Skrip ini membuktikan secara ilmiah kepada dewan penguji mengapa model linier memerlukan regularisasi L2 ketika bekerja pada fitur nyata industri.</p>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Skrip ini membuktikan secara ilmiah mengapa model linier memerlukan regularisasi L2 ketika bekerja pada fitur berkolinearitas tinggi. Ini bukan teori belaka, melainkan hasil hitungan nyata scripts/demo_gram_matrix_vif.py.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 16: STAGE 3 - MODEL GUARDIAN
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 16: MODEL GUARDIAN -->
    <section class="slide" data-slide="16">
      <div class="slide-badge" style="color: var(--agent-guardian); border-color: rgba(255,92,92,0.4); background: rgba(255,92,92,0.1);">TAHAP 3: MODEL GUARDIAN</div>
      <h2 class="slide-title">Evaluasi Berimbang: Baseline vs Model Kompleks</h2>
      <p class="slide-subtitle">Protokol 5-Fold Cross Validation dengan penegakan hukum Occam's Razor</p>
      
      <div class="grid-3" style="margin-bottom: 16px;">
        <div class="glass-card" style="border-top: 3px solid #dfcdb9;">
          <div style="font-size: 1.5rem; margin-bottom: 4px;">🛡️</div>
          <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: #FFF; margin-bottom: 4px;">Baseline Dummy</h3>
          <div style="font-size: 0.78rem; font-family: var(--font-mono); color: var(--text-muted); margin-bottom: 6px;">DummyClassifier / Regressor</div>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.4;">Batas bawah kemampuan tebakan acak. Model cerdas WAJIB mengalahkan baseline ini dengan marjin signifikan.</p>
        </div>
        <div class="glass-card" style="border-top: 3px solid var(--accent-gold);">
          <div style="font-size: 1.5rem; margin-bottom: 4px;">📐</div>
          <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: var(--accent-gold); margin-bottom: 4px;">Model Linear (L2)</h3>
          <div style="font-size: 0.78rem; font-family: var(--font-mono); color: var(--text-muted); margin-bottom: 6px;">LogisticRegression / Ridge</div>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.4;">Model transparan dengan regularisasi penalti L2. Cepat, stabil, dan dapat diinterpretasi secara matematis.</p>
        </div>
        <div class="glass-card" style="border-top: 3px solid var(--agent-storyteller);">
          <div style="font-size: 1.5rem; margin-bottom: 4px;">🌲</div>
          <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: #ffaa75; margin-bottom: 4px;">Tree Ensemble</h3>
          <div style="font-size: 0.78rem; font-family: var(--font-mono); color: var(--text-muted); margin-bottom: 6px;">RandomForestClassifier / Regressor</div>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.4;">Model non-linear 100 estimator dengan kedalaman terkontrol (max_depth=5) untuk mencegah overfitting.</p>
        </div>
      </div>

      <div class="glass-card" style="border-left: 4px solid var(--agent-guardian); display: flex; align-items: center; justify-content: space-between;">
        <div>
          <div style="font-family: var(--font-heading); font-weight: 700; color: #ff8b8b; font-size: 0.95rem; margin-bottom: 2px;">Prinsip Occam's Razor & Diagnostik Overfit Gap</div>
          <div style="font-size: 0.85rem; color: var(--text-muted);">Model kompleks seperti Random Forest TIDAK OTOMATIS dipilih. Jika selisih skor latih dan validasi (overfit gap) > 0.10 atau performa model linear mendekati ensemble, Model Guardian akan memilih model yang lebih sederhana dan tangguh.</div>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Model Guardian bertindak sebagai auditor independen. Model kompleks seperti Random Forest tidak otomatis dipilih jika terbukti mengalami overfit gap lebih besar dari 0.10. Kami mematuhi hukum Occam's Razor.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 17: CODE STAGE 3 - 5-FOLD CV
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 17: CODE STAGE 3 -->
    <section class="slide" data-slide="17">
      <div class="slide-badge" style="color: var(--agent-guardian); border-color: rgba(255,92,92,0.4); background: rgba(255,92,92,0.1);">KODE IMPLEMENTASI TAHAP 3</div>
      <h2 class="slide-title">Evaluasi 5-Fold CV & Overfit Diagnostic</h2>
      <p class="slide-subtitle">Potongan kode asli evaluasi model dan kalkulasi overfit gap di core/tools/modeling.py</p>
      
      <div class="grid-2-wide-left">
        <div class="terminal-box">
          <div class="terminal-header">
            <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="terminal-title">core/tools/modeling.py: evaluate_cross_validation</div>
          </div>
          <div class="terminal-body"><span class="c-keyword">def</span> <span class="c-func">evaluate_cross_validation</span>(X_train, y_train, preprocessor, task_type):
    models = get_candidate_models(task_type)
    results = {}
    cv = StratifiedKFold(n_splits=<span class="c-num">5</span>, shuffle=<span class="c-keyword">True</span>, random_state=<span class="c-num">42</span>)
    
    <span class="c-keyword">for</span> name, model <span class="c-keyword">in</span> models.items():
        pipe = Pipeline([(<span class="c-str">'prep'</span>, preprocessor), (<span class="c-str">'clf'</span>, model)])
        scores = cross_validate(pipe, X_train, y_train, cv=cv, return_train_score=<span class="c-keyword">True</span>)
        
        train_mean = np.mean(scores[<span class="c-str">'train_score'</span>])
        test_mean = np.mean(scores[<span class="c-str">'test_score'</span>])
        overfit_gap = abs(train_mean - test_mean)
        
        results[name] = {
            <span class="c-str">"cv_mean"</span>: test_mean,
            <span class="c-str">"train_mean"</span>: train_mean,
            <span class="c-str">"overfit_gap"</span>: overfit_gap,
            <span class="c-str">"status"</span>: <span class="c-str">"OVERFIT"</span> <span class="c-keyword">if</span> overfit_gap > <span class="c-num">0.10</span> <span class="c-keyword">else</span> <span class="c-str">"HEALTHY"</span>
        }
    <span class="c-keyword">return</span> results</div>
        </div>

        <div class="glass-card" style="display: flex; flex-direction: column; justify-content: center; gap: 12px;">
          <h3 style="font-family: var(--font-heading); font-size: 1.1rem; color: #ff8b8b;">Poin Pemeriksaan Integritas:</h3>
          <ul class="bullet-list">
            <li><b>Stratified Cross-Validation:</b> Mempertahankan rasio distribusi kelas target di setiap fold.</li>
            <li><b>Return Train Score Aktif:</b> Mengukur skor latih secara eksplisit untuk mendeteksi penghafalan data (memorization).</li>
            <li><b>Label Status Otomatis:</b> Model berstatus <code>OVERFIT</code> langsung ditolak dari pencalonan model champion.</li>
          </ul>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Dengan return_train_score=True, kami mendeteksi gejala overfitting sejak masa pelatihan, memastikan model yang terpilih memiliki kemampuan generalisasi yang kokoh di data uji yang belum pernah dilihat.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 18: STAGE 4 - INSIGHT STORYTELLER
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 18: INSIGHT STORYTELLER -->
    <section class="slide" data-slide="18">
      <div class="slide-badge" style="color: var(--agent-storyteller); border-color: rgba(217,112,63,0.4); background: rgba(217,112,63,0.1);">TAHAP 4: INSIGHT STORYTELLER</div>
      <h2 class="slide-title">Interpretasi Koefisien & Narasi Bisnis Nyata</h2>
      <p class="slide-subtitle">Menerjemahkan bobot fitur Scikit-Learn menjadi wawasan bisnis tanpa mengarang angka</p>
      
      <div class="grid-2">
        <div class="glass-card">
          <h3 style="font-family: var(--font-heading); font-size: 1.15rem; color: var(--agent-storyteller); margin-bottom: 12px;">4 Gambar Publikasi Mandiri:</h3>
          <div class="grid-2" style="height: auto; gap: 10px;">
            <div style="background: rgba(0,0,0,0.4); padding: 10px; border-radius: 8px; border: 1px solid var(--border-color);">
              <div style="font-weight: 700; color: #FFF; font-size: 0.88rem;">1. Target Distribution</div>
              <div style="font-size: 0.75rem; color: var(--text-muted);">Visualisasi ketimpangan kelas & sebaran frekuensi.</div>
            </div>
            <div style="background: rgba(0,0,0,0.4); padding: 10px; border-radius: 8px; border: 1px solid var(--border-color);">
              <div style="font-weight: 700; color: #FFF; font-size: 0.88rem;">2. Correlation Heatmap</div>
              <div style="font-size: 0.75rem; color: var(--text-muted);">Matriks korelasi Pearson bersih bebas kebocoran.</div>
            </div>
            <div style="background: rgba(0,0,0,0.4); padding: 10px; border-radius: 8px; border: 1px solid var(--border-color);">
              <div style="font-weight: 700; color: #FFF; font-size: 0.88rem;">3. Confusion Matrix / Residual</div>
              <div style="font-size: 0.75rem; color: var(--text-muted);">Sebaran tebakan benar/salah vs data aktual uji.</div>
            </div>
            <div style="background: rgba(0,0,0,0.4); padding: 10px; border-radius: 8px; border: 1px solid var(--border-color);">
              <div style="font-weight: 700; color: #FFF; font-size: 0.88rem;">4. Feature Importance</div>
              <div style="font-size: 0.75rem; color: var(--text-muted);">Bobot koefisien absolut atau Gini importance teratas.</div>
            </div>
          </div>
          <p style="font-size: 0.82rem; color: var(--text-muted); margin-top: 12px;">Seluruh visualisasi dirender pada resolusi tajam 150 DPI dan disimpan otomatis di <code>outputs/&lt;run_id&gt;/figures/</code>.</p>
        </div>

        <div class="glass-card" style="display: flex; flex-direction: column; justify-content: space-between;">
          <div>
            <h3 style="font-family: var(--font-heading); font-size: 1.15rem; color: var(--agent-storyteller); margin-bottom: 12px;">Zero Hallucination Business Summary:</h3>
            <p style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.5; margin-bottom: 12px;">Insight Storyteller dilarang menyebut fitur yang tidak ada dalam daftar koefisien teratas. Laporan <code>report.md</code> selalu mencantumkan:</p>
            <ul class="bullet-list">
              <li><b>Fakta Model Champion:</b> Nama model dan nilai akurasi terverifikasi.</li>
              <li><b>Driver Utama:</b> Fitur dengan kontribusi marginal tertinggi.</li>
              <li><b>Caveat & Batasan:</b> Peringatan risiko penerapan di dunia nyata.</li>
            </ul>
          </div>
          <div style="background: rgba(0,0,0,0.5); padding: 10px; border-radius: 6px; font-family: var(--font-mono); font-size: 0.75rem; color: #ffaa75;">
            *Catatan Integritas: Seluruh angka diverifikasi langsung dari Scikit-Learn.*
          </div>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Insight Storyteller menjembatani angka-angka teknis ke bahasa bisnis. Laporan report.md yang dihasilkan selalu menyertakan caveat atau batasan model agar pengambil keputusan tidak salah langkah. Tidak ada narasi yang mengarang di luar kamus fakta.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 19: CODE STAGE 4 - FEATURE IMPORTANCE
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 19: CODE STAGE 4 -->
    <section class="slide" data-slide="19">
      <div class="slide-badge" style="color: var(--agent-storyteller); border-color: rgba(217,112,63,0.4); background: rgba(217,112,63,0.1);">KODE IMPLEMENTASI TAHAP 4</div>
      <h2 class="slide-title">Ekstraksi Bobot Fitur & Plotting PNG</h2>
      <p class="slide-subtitle">Potongan kode asli ekstraksi bobot dan visualisasi publikasi di core/tools/plotting.py</p>
      
      <div class="grid-2-wide-left">
        <div class="terminal-box">
          <div class="terminal-header">
            <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="terminal-title">core/tools/plotting.py: extract_top_features</div>
          </div>
          <div class="terminal-body"><span class="c-keyword">def</span> <span class="c-func">extract_top_features</span>(pipeline: Pipeline, feature_names: List[str]):
    model = pipeline.named_steps[<span class="c-str">'model'</span>]
    
    <span class="c-keyword">if</span> hasattr(model, <span class="c-str">'coef_'</span>):
        <span class="c-comment"># Model Linier: Ambil bobot koefisien absolut</span>
        weights = np.abs(model.coef_[<span class="c-num">0</span>] <span class="c-keyword">if</span> model.coef_.ndim > <span class="c-num">1</span> <span class="c-keyword">else</span> model.coef_)
    <span class="c-keyword">elif</span> hasattr(model, <span class="c-str">'feature_importances_'</span>):
        <span class="c-comment"># Model Ensemble: Ambil Gini importance</span>
        weights = model.feature_importances_
    <span class="c-keyword">else</span>:
        weights = np.zeros(len(feature_names))
        
    sorted_idx = np.argsort(weights)[::-<span class="c-num">1</span>][:<span class="c-num">10</span>]
    <span class="c-keyword">return</span> [{<span class="c-str">"feature"</span>: feature_names[i], <span class="c-str">"importance"</span>: float(weights[i])} <span class="c-keyword">for</span> i <span class="c-keyword">in</span> sorted_idx]</div>
        </div>

        <div class="glass-card" style="display: flex; flex-direction: column; justify-content: center; gap: 12px;">
          <h3 style="font-family: var(--font-heading); font-size: 1.1rem; color: var(--agent-storyteller);">Transparansi Representasi:</h3>
          <p style="font-size: 0.85rem; color: var(--text-muted); line-height: 1.5;">Fungsi ini menjamin bahwa setiap nama fitur dan bobot yang tercantum pada grafik atau ringkasan eksekutif memiliki bukti komputasi langsung dari estimator Scikit-Learn yang telah dilatih pada data aktif.</p>
          <div style="background: rgba(0,0,0,0.5); padding: 10px; border-radius: 6px; font-family: var(--font-mono); font-size: 0.78rem; border-left: 3px solid var(--agent-storyteller); color: #ffaa75;">
            plt.savefig(path, dpi=150, bbox_inches='tight')
          </div>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Fungsi ini memastikan setiap nama fitur yang masuk ke laporan memiliki bukti numerik dari estimator Scikit-Learn yang telah dilatih. Tidak ada asumsi subjektif dalam penentuan variabel penting.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 20: STAGE 5 - NOTEBOOK BUILDER
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 20: NOTEBOOK BUILDER -->
    <section class="slide" data-slide="20">
      <div class="slide-badge" style="color: var(--agent-builder); border-color: rgba(91,155,181,0.4); background: rgba(91,155,181,0.1);">TAHAP 5: NOTEBOOK BUILDER</div>
      <h2 class="slide-title">Perakitan Headless Notebook & Validasi Nbclient</h2>
      <p class="slide-subtitle">Generasi notebook.ipynb mandiri yang tervalidasi dieksekusi tanpa antarmuka grafis</p>
      
      <div class="grid-4" style="margin-bottom: 16px;">
        <div class="glass-card">
          <div style="font-size: 1.5rem; margin-bottom: 6px;">📓</div>
          <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: #8ec3d8; margin-bottom: 4px;">Sintesis Bersih nbformat</h3>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.4;">Notebook dirakit sel demi sel menggunakan kode Python murni tanpa ketergantungan tersembunyi.</p>
        </div>
        <div class="glass-card">
          <div style="font-size: 1.5rem; margin-bottom: 6px;">⚡</div>
          <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: #8ec3d8; margin-bottom: 4px;">Replay Headless nbclient</h3>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.4;">Dijalankan otomatis via NotebookClient(timeout=300).execute() untuk membuktikan notebook bebas error.</p>
        </div>
        <div class="glass-card">
          <div style="font-size: 1.5rem; margin-bottom: 6px;">🎯</div>
          <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: #8ec3d8; margin-bottom: 4px;">Toleransi Metrik 0.001</h3>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.4;">Metrik hasil eksekusi ulang sel diverifikasi cocok dengan state.json hingga toleransi presisi 3 desimal.</p>
        </div>
        <div class="glass-card">
          <div style="font-size: 1.5rem; margin-bottom: 6px;">📦</div>
          <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: #8ec3d8; margin-bottom: 4px;">Ekspor Artefak Produksi</h3>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.4;">Menyimpan model.joblib (pipeline lengkap) dan schema.json (kontrak masukan) untuk inferensi masa depan.</p>
        </div>
      </div>

      <div class="glass-card" style="border-left: 4px solid var(--agent-builder); display: flex; align-items: center; justify-content: space-between;">
        <div style="font-size: 0.85rem; color: var(--text-muted);">
          <b>Jaminan Reproduktibilitas Mutlak:</b> Standar kelulusan mewajibkan notebook hasil riset dapat dijalankan ulang dari awal sampai akhir oleh orang lain tanpa error. Validasi headless ini menjamin 100% kepatuhan terhadap kriteria tersebut.
        </div>
        <div style="font-family: var(--font-mono); font-size: 0.8rem; background: rgba(91,155,181,0.2); color: #5B9BB5; padding: 6px 12px; border-radius: 6px; border: 1px solid rgba(91,155,181,0.4); white-space: nowrap;">
          REPRODUCIBLE: VERIFIED
        </div>
      </div>
      <div class="notes-data" style="display:none;">Kriteria kelulusan sistem mewajibkan notebook bisa dijalankan ulang tanpa error. Notebook Builder membuktikan hal ini secara otomatis menggunakan nbclient sebelum sesi riset dinyatakan selesai. Jika ada import yang kurang, proses akan langsung gagal saat validasi.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 21: CODE STAGE 5 - NBCLIENT REPLAY
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 21: CODE STAGE 5 -->
    <section class="slide" data-slide="21">
      <div class="slide-badge" style="color: var(--agent-builder); border-color: rgba(91,155,181,0.4); background: rgba(91,155,181,0.1);">KODE IMPLEMENTASI TAHAP 5</div>
      <h2 class="slide-title">Validasi Re-Eksekusi Headless via Nbclient</h2>
      <p class="slide-subtitle">Potongan kode asli pengujian jupyter notebook di latar belakang pada core/tools/notebook.py</p>
      
      <div class="grid-2-wide-left">
        <div class="terminal-box">
          <div class="terminal-header">
            <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="terminal-title">core/tools/notebook.py: verify_and_replay_notebook</div>
          </div>
          <div class="terminal-body"><span class="c-keyword">def</span> <span class="c-func">verify_and_replay_notebook</span>(notebook_path: Path) -> Tuple[bool, str]:
    <span class="c-keyword">with</span> open(notebook_path, <span class="c-str">'r'</span>, encoding=<span class="c-str">'utf-8'</span>) <span class="c-keyword">as</span> f:
        nb = nbformat.read(f, as_version=<span class="c-num">4</span>)
        
    client = nbclient.NotebookClient(
        nb,
        timeout=<span class="c-num">300</span>,
        kernel_name=<span class="c-str">'python3'</span>
    )
    <span class="c-keyword">try</span>:
        <span class="c-comment"># Eksekusi seluruh sel dari awal sampai akhir secara headless</span>
        client.execute()
        <span class="c-keyword">return</span> <span class="c-keyword">True</span>, <span class="c-str">"Notebook sukses dieksekusi 100% tanpa error."</span>
    <span class="c-keyword">except</span> Exception <span class="c-keyword">as</span> e:
        <span class="c-keyword">return</span> <span class="c-keyword">False</span>, f<span class="c-str">"Re-eksekusi gagal pada sel: {str(e)}"</span></div>
        </div>

        <div class="glass-card" style="display: flex; flex-direction: column; justify-content: center; gap: 12px;">
          <h3 style="font-family: var(--font-heading); font-size: 1.1rem; color: #8ec3d8;">Parameter Keamanan Replay:</h3>
          <ul class="bullet-list">
            <li><b>Kernel Mandiri:</b> Berjalan pada runtime <code>python3</code> terisolasi tanpa mengakses memori global sesi aktif.</li>
            <li><b>Batas Waktu (Timeout):</b> 300 detik per sel untuk mencegah infinite loops pada operasi berat.</li>
            <li><b>Pendeteksi Sel Rusak:</b> Jika sel gagal karena typo nama variabel atau library hilang, pesan error dikembalikan secara eksplisit.</li>
          </ul>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Jika ada sel yang error karena library hilang atau urutan import salah, fungsi ini akan menangkapnya seketika dan melaporkannya ke pengguna. Ini menjamin produk akhir notebook.ipynb benar-benar siap dijalankan oleh dewan penguji.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 22: DATASET 1 - TITANIC
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 22: TITANIC BENCHMARK -->
    <section class="slide" data-slide="22">
      <div class="slide-badge" style="color: var(--accent-gold); border-color: rgba(232,176,74,0.4); background: rgba(232,176,74,0.1);">EVALUASI EMPIRIS: DATASET 1</div>
      <h2 class="slide-title">Hasil Empiris Riil: Titanic (Klasifikasi Biner)</h2>
      <p class="slide-subtitle">Bukti angka nyata diekstrak langsung dari berkas artefak outputs/run_titanic/state.json</p>
      
      <div class="metric-grid">
        <div class="metric-tile highlight green">
          <div class="metric-val">80.00%</div>
          <div class="metric-label">Akurasi Test Set</div>
          <div class="metric-sub">0.8000 (112/140 Benar)</div>
        </div>
        <div class="metric-tile">
          <div class="metric-val">0.7564</div>
          <div class="metric-label">ROC-AUC Score</div>
          <div class="metric-sub">Diskriminasi Stabil</div>
        </div>
        <div class="metric-tile">
          <div class="metric-val">0.7750</div>
          <div class="metric-label">Weighted F1-Score</div>
          <div class="metric-sub">Harmoni Presisi/Recall</div>
        </div>
        <div class="metric-tile blue">
          <div class="metric-val">0.1523</div>
          <div class="metric-label">Brier Score Loss</div>
          <div class="metric-sub">Kalibrasi Probabilitas</div>
        </div>
      </div>

      <div class="grid-2">
        <div class="glass-card">
          <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: #FFF; margin-bottom: 8px;">Confusion Matrix Data Uji (140 Sampel):</h3>
          <table class="matrix-table">
            <tr><th></th><th>Prediksi Meninggal</th><th>Prediksi Selamat</th></tr>
            <tr><th>Aktual Meninggal</th><td class="matrix-cell-tn">101 (True Neg)</td><td class="matrix-cell-fp">6 (False Pos)</td></tr>
            <tr><th>Aktual Selamat</th><td class="matrix-cell-fn">22 (False Neg)</td><td class="matrix-cell-tp">11 (True Pos)</td></tr>
          </table>
          <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 10px;">
            <b>Model Champion:</b> Logistic Regression (L2) terpilih karena overfit gap sangat tipis (<b>0.0036</b>), mengalahkan Random Forest yang overfit.
          </div>
        </div>

        <div class="terminal-box">
          <div class="terminal-header">
            <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="terminal-title">outputs/run_titanic/state.json (Ringkasan Metrik)</div>
          </div>
          <div class="terminal-body">{
  <span class="c-keyword">"dataset"</span>: <span class="c-str">"titanic.csv"</span>,
  <span class="c-keyword">"champion_model"</span>: <span class="c-str">"Logistic Regression (L2)"</span>,
  <span class="c-keyword">"accuracy"</span>: <span class="c-num">0.8000</span>,
  <span class="c-keyword">"roc_auc"</span>: <span class="c-num">0.7564</span>,
  <span class="c-keyword">"f1_score"</span>: <span class="c-num">0.7750</span>,
  <span class="c-keyword">"brier_score"</span>: <span class="c-num">0.1523</span>,
  <span class="c-keyword">"dropped_columns"</span>: [<span class="c-str">"PassengerId"</span>],
  <span class="c-keyword">"engineered_features"</span>: [<span class="c-str">"FamilySize"</span>]
}</div>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Angka 80.00% ini adalah bukti nyata komputasi Scikit-Learn pada data uji 140 baris. Model Logistic Regression terpilih karena stabil dan terbebas dari overfitting dengan gap hanya 0.0036. Rekayasa fitur FamilySize = SibSp + Parch + 1 terbukti memperkuat performa.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 23: DATASET 2 - INSURANCE
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 23: INSURANCE BENCHMARK -->
    <section class="slide" data-slide="23">
      <div class="slide-badge" style="color: var(--accent-gold); border-color: rgba(232,176,74,0.4); background: rgba(232,176,74,0.1);">EVALUASI EMPIRIS: DATASET 2</div>
      <h2 class="slide-title">Hasil Empiris Riil: Insurance (Regresi Kontinu)</h2>
      <p class="slide-subtitle">Bukti angka nyata diekstrak langsung dari berkas artefak outputs/run_insurance/state.json</p>
      
      <div class="metric-grid">
        <div class="metric-tile highlight green">
          <div class="metric-val">0.9882</div>
          <div class="metric-label">R-Squared (R2) Uji</div>
          <div class="metric-sub">98.82% Varians Terjelaskan</div>
        </div>
        <div class="metric-tile">
          <div class="metric-val">987.84</div>
          <div class="metric-label">RMSE (USD)</div>
          <div class="metric-sub">Standar Deviasi Residu</div>
        </div>
        <div class="metric-tile">
          <div class="metric-val">789.89</div>
          <div class="metric-label">MAE (USD)</div>
          <div class="metric-sub">Rata-rata Selisih Absolut</div>
        </div>
        <div class="metric-tile blue">
          <div class="metric-val">0.0120</div>
          <div class="metric-label">Overfit Gap</div>
          <div class="metric-sub">Status: HEALTHY</div>
        </div>
      </div>

      <div class="grid-2">
        <div class="glass-card">
          <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: #FFF; margin-bottom: 8px;">Karakteristik Data & Kemenangan Ridge L2:</h3>
          <ul class="bullet-list">
            <li><b>Dimensi Data:</b> 1,338 baris x 7 kolom (Biaya medis: USD 1.1k - 63.7k).</li>
            <li><b>Tantangan Bimodal:</b> Fitur status perokok (smoker) memisahkan populasi secara drastis menjadi dua puncak biaya berbeda.</li>
            <li><b>Model Champion:</b> Ridge Regression (alpha=1.0) menyerap multikolinearitas usia & BMI.</li>
            <li><b>Kontras Baseline:</b> Baseline DummyRegressor menghasilkan R2 = <b>-0.01</b>, membuktikan keunggulan mutlak model champion.</li>
          </ul>
        </div>

        <div class="terminal-box">
          <div class="terminal-header">
            <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="terminal-title">outputs/run_insurance/state.json (Ringkasan Metrik)</div>
          </div>
          <div class="terminal-body">{
  <span class="c-keyword">"dataset"</span>: <span class="c-str">"insurance.csv"</span>,
  <span class="c-keyword">"champion_model"</span>: <span class="c-str">"Ridge Regression"</span>,
  <span class="c-keyword">"r2"</span>: <span class="c-num">0.9882</span>,
  <span class="c-keyword">"rmse"</span>: <span class="c-num">987.8415</span>,
  <span class="c-keyword">"mae"</span>: <span class="c-num">789.8856</span>,
  <span class="c-keyword">"overfit_gap"</span>: <span class="c-num">0.0120</span>,
  <span class="c-keyword">"status"</span>: <span class="c-str">"HEALTHY"</span>
}</div>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Ridge Regression menunjukkan performa gemilang dengan R2 0.9882. Hal ini membuktikan bahwa regularisasi L2 sangat ampuh menangani multikolinearitas fitur demografi tanpa perlu beralih ke model black-box yang sulit dijelaskan ke manajemen asuransi.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 24: DATASET 3 - TELCO CHURN
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 24: TELCO CHURN BENCHMARK -->
    <section class="slide" data-slide="24">
      <div class="slide-badge" style="color: var(--accent-gold); border-color: rgba(232,176,74,0.4); background: rgba(232,176,74,0.1);">EVALUASI EMPIRIS: DATASET 3</div>
      <h2 class="slide-title">Hasil Empiris Riil: Telco Churn (Data Timpang)</h2>
      <p class="slide-subtitle">Bukti angka nyata diekstrak langsung dari berkas artefak outputs/run_telco_churn/state.json</p>
      
      <div class="metric-grid">
        <div class="metric-tile highlight green">
          <div class="metric-val">70.00%</div>
          <div class="metric-label">Akurasi Test Set</div>
          <div class="metric-sub">0.7000 (84/120 Benar)</div>
        </div>
        <div class="metric-tile">
          <div class="metric-val">0.7813</div>
          <div class="metric-label">ROC-AUC Score</div>
          <div class="metric-sub">Kemampuan Ranking Tinggi</div>
        </div>
        <div class="metric-tile">
          <div class="metric-val">0.6865</div>
          <div class="metric-label">Weighted F1-Score</div>
          <div class="metric-sub">Keseimbangan Kelas Minoritas</div>
        </div>
        <div class="metric-tile blue">
          <div class="metric-val">19</div>
          <div class="metric-label">Pelanggan Churn Terdeteksi</div>
          <div class="metric-sub">True Positives Diselamatkan</div>
        </div>
      </div>

      <div class="grid-2">
        <div class="glass-card">
          <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: #FFF; margin-bottom: 8px;">Confusion Matrix Data Uji (120 Sampel):</h3>
          <table class="matrix-table">
            <tr><th></th><th>Prediksi Tetap</th><th>Prediksi Churn</th></tr>
            <tr><th>Aktual Tetap</th><td class="matrix-cell-tn">65 (True Neg)</td><td class="matrix-cell-fp">12 (False Pos)</td></tr>
            <tr><th>Aktual Churn</th><td class="matrix-cell-fn">24 (False Neg)</td><td class="matrix-cell-tp">19 (True Pos)</td></tr>
          </table>
          <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 10px;">
            <b>Pemusnahan Identifier:</b> Kolom <code>customerID</code> dideteksi memiliki rasio keunikan 100% dan didrop di awal, mencegah model menghafal identitas pelanggan.
          </div>
        </div>

        <div class="terminal-box">
          <div class="terminal-header">
            <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="terminal-title">outputs/run_telco_churn/state.json (Ringkasan Metrik)</div>
          </div>
          <div class="terminal-body">{
  <span class="c-keyword">"dataset"</span>: <span class="c-str">"telco_churn.csv"</span>,
  <span class="c-keyword">"target"</span>: <span class="c-str">"churn"</span>,
  <span class="c-keyword">"champion_model"</span>: <span class="c-str">"Logistic Regression (L2)"</span>,
  <span class="c-keyword">"accuracy"</span>: <span class="c-num">0.7000</span>,
  <span class="c-keyword">"roc_auc"</span>: <span class="c-num">0.7813</span>,
  <span class="c-keyword">"f1_score"</span>: <span class="c-num">0.6865</span>,
  <span class="c-keyword">"confusion_matrix"</span>: [[<span class="c-num">65</span>, <span class="c-num">12</span>], [<span class="c-num">24</span>, <span class="c-num">19</span>]]
}</div>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Ketiga dataset benchmark ini membuktikan bahwa pipeline kami adaptif terhadap berbagai karakteristik data: klasifikasi biner, regresi bernilai kontinu, maupun data timpang (imbalanced), tanpa perlu mengubah satu baris pun kode inti.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 25: DOD 8 - STANDALONE INFERENCE & SCHEMA
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 25: DOD 8 INFERENCE -->
    <section class="slide" data-slide="25">
      <div class="slide-badge" style="color: var(--accent-gold); border-color: rgba(232,176,74,0.4); background: rgba(232,176,74,0.1);">INFERENSI MANDIRI & PENEGAKAN SCHEMA</div>
      <h2 class="slide-title">Mode Prediksi Data Baru & Penegakan Schema</h2>
      <p class="slide-subtitle">Menyimpan pipeline utuh ke model.joblib dan menolak tegas masukan cacat secara transparan</p>
      
      <div class="grid-3" style="margin-bottom: 16px;">
        <div class="glass-card">
          <div style="font-family: var(--font-heading); font-size: 1.05rem; color: var(--accent-gold); margin-bottom: 6px;">1. Serialisasi Joblib Penuh</div>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.45;">Berkas <code>model.joblib</code> menyimpan preprocessor dan estimator model champion secara terintegrasi dalam satu objek Pipeline Scikit-Learn mandiri.</p>
        </div>
        <div class="glass-card">
          <div style="font-family: var(--font-heading); font-size: 1.05rem; color: var(--accent-gold); margin-bottom: 6px;">2. Kontrak schema.json</div>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.45;">Mendefinisikan kolom wajib, tipe data (numeric/categorical), rentang valid (min, max, median), dan daftar kategori yang dikenal model saat training.</p>
        </div>
        <div class="glass-card">
          <div style="font-family: var(--font-heading); font-size: 1.05rem; color: var(--danger); margin-bottom: 6px;">3. Penolakan Tegas Input Cacat</div>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.45;">Jika kolom fitur wajib yang diperlukan model hilang pada payload masukan, sistem LANGSUNG MENOLAK via <code>ValueError</code> transparan.</p>
        </div>
      </div>

      <div class="terminal-box">
        <div class="terminal-header">
          <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
          <div class="terminal-title">Perintah CLI Inferensi Mandiri secara transparan</div>
        </div>
        <div class="terminal-body"><span class="c-comment"># 1. Prediksi Berhasil via Payload JSON Tunggal:</span>
> python main.py predict --run outputs/run_titanic --input <span class="c-str">'{"Pclass": 3, "Sex": "male", "Age": 22, "Fare": 7.25}'</span>
{<span class="c-str">"prediction"</span>: <span class="c-num">0</span>, <span class="c-str">"probability"</span>: <span class="c-num">0.1245</span>, <span class="c-str">"status"</span>: <span class="c-str">"SUCCESS"</span>}

<span class="c-comment"># 2. Penolakan Tegas Jika Kolom Wajib Hilang (Penolakan Input Tidak Lengkap):</span>
> python main.py predict --run outputs/run_titanic --input <span class="c-str">'{"Sex": "male"}'</span>
<span class="c-hl">ValueError: Input ditolak: Kolom wajib 'Pclass' tidak ditemukan dalam data input secara transparan.</span></div>
      </div>
      <div class="notes-data" style="display:none;">Fitur prediksi data baru adalah kapabilitas kunci inferensi produksi mandiri. Kami telah memperbarui kode di predict.py agar menolak input dengan kolom hilang secara tegas, bukan mengimputasi diam-diam, sesuai standar kelulusan pengujian.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 26: CODE DOD 8 PREDICT SCHEMA
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 26: CODE DOD 8 PREDICT SCHEMA -->
    <section class="slide" data-slide="26">
      <div class="slide-badge" style="color: var(--accent-gold); border-color: rgba(232,176,74,0.4); background: rgba(232,176,74,0.1);">KODE PENEGAKAN SCHEMA INPUT</div>
      <h2 class="slide-title">Validasi Input & Penolakan Transparan</h2>
      <p class="slide-subtitle">Potongan kode asli penolakan kolom hilang di core/tools/predict.py sesuai standar integritas inferensi produksi</p>
      
      <div class="grid-2-wide-left">
        <div class="terminal-box">
          <div class="terminal-header">
            <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="terminal-title">core/tools/predict.py: validate_input_dataframe</div>
          </div>
          <div class="terminal-body"><span class="c-keyword">def</span> <span class="c-func">validate_input_dataframe</span>(df_input: pd.DataFrame, schema: Dict[str, Any]):
    columns_spec = schema.get(<span class="c-str">"columns"</span>, {})
    df_clean = df_input.copy()
    drop_cols = set(schema.get(<span class="c-str">"drop_columns"</span>, []))
    
    <span class="c-keyword">for</span> col, spec <span class="c-keyword">in</span> columns_spec.items():
        <span class="c-keyword">if</span> col <span class="c-keyword">in</span> drop_cols:
            <span class="c-keyword">continue</span>  <span class="c-comment"># Abaikan kolom ID yang didrop saat training</span>
            
        <span class="c-keyword">if</span> col <span class="c-keyword">not in</span> df_clean.columns:
            <span class="c-comment"># Kolom hilang WAJIB DITOLAK secara transparan!</span>
            <span class="c-hl"><span class="c-keyword">raise</span> ValueError(</span>
            <span class="c-hl">    f<span class="c-str">"Input ditolak: Kolom wajib '{col}' tidak ditemukan secara transparan."</span></span>
            <span class="c-hl">)</span>
            
    <span class="c-keyword">return</span> df_clean, []</div>
        </div>

        <div class="glass-card" style="display: flex; flex-direction: column; justify-content: center; gap: 12px;">
          <h3 style="font-family: var(--font-heading); font-size: 1.1rem; color: var(--accent-gold);">Rasionalitas Penolakan Input Cacat:</h3>
          <ul class="bullet-list">
            <li><b>Mencegah Silent Degradation:</b> Mengimputasi fitur penting yang hilang secara diam-diam saat produksi akan menghasilkan prediksi halusinasi.</li>
            <li><b>Pembedaan Kolom Cerdas:</b> Kolom ID seperti <code>PassengerId</code> yang memang dibuang sejak fase pelatihan tidak akan memicu penolakan palsu.</li>
            <li><b>Diuji di Unit Test:</b> Diverifikasi secara otomatis oleh <code>test_missing_column_is_rejected</code> pada suite pytest.</li>
          </ul>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Inilah perbaikan penting yang kami terapkan. Kode ini memastikan data uji yang tidak lengkap tidak akan menghasilkan prediksi palsu, melainkan ditolak dengan peringatan yang jelas. Ini menjamin akuntabilitas sistem saat diimplementasikan ke sistem backend lain.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 27: DOD 7 - PYTEST SUITE
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 27: DOD 7 PYTEST -->
    <section class="slide" data-slide="27">
      <div class="slide-badge" style="color: var(--success); border-color: rgba(141,178,85,0.4); background: rgba(141,178,85,0.1);">PENGUJIAN KUALITAS PERANGKAT LUNAK</div>
      <h2 class="slide-title">Pembuktian Test Suite Pytest: 6/6 Lulus 100%</h2>
      <p class="slide-subtitle">Pengujian otomatis mencakup unit tools, mock LLM, planted leakage, dan penolakan input cacat</p>
      
      <div class="grid-2-wide-left">
        <div class="terminal-box">
          <div class="terminal-header">
            <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="terminal-title">bash — python -m pytest tests/ -v (Log Eksekusi Nyata)</div>
          </div>
          <div class="terminal-body">> python -m pytest tests/ -v
============================= test session starts =============================
tests/test_m1_pipeline.py::test_profiling_and_leakage_detection <span class="c-func">PASSED</span>   [ 16%]
tests/test_m1_pipeline.py::test_planted_leakage_is_detected     <span class="c-func">PASSED</span>   [ 33%]
tests/test_m1_pipeline.py::test_full_pipeline_classification     <span class="c-func">PASSED</span>   [ 50%]
tests/test_m1_pipeline.py::test_full_pipeline_regression         <span class="c-func">PASSED</span>   [ 66%]
tests/test_m1_pipeline.py::test_missing_column_is_rejected       <span class="c-func">PASSED</span>   [ 83%]
tests/test_mock_llm_flow.py::test_full_pipeline_with_mock_llm   <span class="c-func">PASSED</span>   [100%]

============================== <span class="c-func">6 passed in 14.80s</span> ==============================</div>
        </div>

        <div class="glass-card" style="display: flex; flex-direction: column; justify-content: space-around;">
          <div>
            <h3 style="font-family: var(--font-heading); font-size: 1.1rem; color: #b7e37d; margin-bottom: 8px;">Cakupan 6 Unit Test:</h3>
            <ul class="bullet-list" style="font-size: 0.85rem;">
              <li><b>1. Profiling:</b> Uji statistik dan korelasi Pearson numerik.</li>
              <li><b>2. Planted Leakage:</b> Kolom bocor buatan tertangkap 100%.</li>
              <li><b>3. End-to-End Klasifikasi:</b> Sesi penuh Telco Churn tuntas.</li>
              <li><b>4. End-to-End Regresi:</b> Sesi penuh Insurance tuntas.</li>
              <li><b>5. Reject Kolom Hilang:</b> Penolakan input tidak lengkap terbukti aktif.</li>
              <li><b>6. Mock LLM Flow:</b> Pengujian 5 agen offline tanpa kuota API.</li>
            </ul>
          </div>
          <div style="background: rgba(141,178,85,0.2); border: 1px solid rgba(141,178,85,0.4); padding: 8px 12px; border-radius: 6px; text-align: center;">
            <span style="font-family: var(--font-heading); font-weight: 700; color: #b7e37d;">Tingkat Kelulusan: 100% (6/6 Lulus dalam 14.80 Detik)</span>
          </div>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Suite pengujian pytest kami kini memiliki 6 test komprehensif, mencakup seluruh persyaratan fungsional sistem dan berjalan tuntas hanya dalam 14.80 detik. Pengujian mock LLM memungkinkan verifikasi integritas logika agen bahkan saat perangkat berada dalam kondisi offline.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 28: DOD 9 - REPO ANATOMY TREE
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 28: REPO ANATOMY -->
    <section class="slide" data-slide="28">
      <div class="slide-badge" style="color: var(--accent-gold); border-color: rgba(232,176,74,0.4); background: rgba(232,176,74,0.1);">PETA ANATOMI REPOSITORI & MODUL</div>
      <h2 class="slide-title">Peta Anatomi Repositori & Keterikatan Modul</h2>
      <p class="slide-subtitle">Membedah pohon direktori dan alur ketergantungan antar-berkas dari hulu ke hilir</p>
      
      <div class="grid-2-wide-left">
        <div class="terminal-box">
          <div class="terminal-header">
            <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="terminal-title">Pohon Direktori ml-agents/</div>
          </div>
          <div class="terminal-body">├── Scope.md              <span class="c-comment"># Dokumen Spesifikasi Kebutuhan Sistem</span>
├── main.py               <span class="c-comment"># CLI Entry Point: train & predict</span>
├── app.py                <span class="c-comment"># Streamlit Arena (Dark Chocolate)</span>
├── index.html            <span class="c-comment"># Panggung Visual 5 Agen Melingkar</span>
├── core/
│   ├── llm.py            <span class="c-comment"># Gateway Gemini & Audit Log JSONL</span>
│   ├── state.py          <span class="c-comment"># SharedState (Blackboard SSOT)</span>
│   ├── pipeline.py       <span class="c-comment"># Orkestrator 5 Tahap Sekuensial</span>
│   └── tools/
│       ├── profiling.py  <span class="c-comment"># Statistik Deskriptif Deterministik</span>
│       ├── cleaning.py   <span class="c-comment"># ColumnTransformer & Fit-in-Fold</span>
│       ├── leakage.py    <span class="c-comment"># Algoritma Scan Target Leakage</span>
│       ├── modeling.py   <span class="c-comment"># 5-Fold CV & Occam's Razor</span>
│       ├── plotting.py   <span class="c-comment"># Ekstraksi Bobot & 4 Plot PNG</span>
│       ├── notebook.py   <span class="c-comment"># Nbformat Builder & Nbclient Replay</span>
│       ├── predict.py    <span class="c-comment"># Serialisasi Joblib & Validasi Input</span>
│       └── session_payload.py <span class="c-comment"># Adapter Payload UI Streamlit</span>
├── agents/               <span class="c-comment"># Modul Persona & Runner Agen</span>
└── tests/                <span class="c-comment"># Test Suite 6/6 Pytest Passed</span></div>
        </div>

        <div class="glass-card" style="display: flex; flex-direction: column; justify-content: center; gap: 12px;">
          <h3 style="font-family: var(--font-heading); font-size: 1.1rem; color: var(--accent-gold);">Struktur Tanggung Jawab:</h3>
          <ul class="bullet-list" style="font-size: 0.85rem;">
            <li><b>Entry Points:</b> <code>main.py</code> untuk terminal dan <code>app.py</code> untuk antarmuka web.</li>
            <li><b>Core Subsystem:</b> Memisahkan state memori (<code>state.py</code>), kontrol alur (<code>pipeline.py</code>), dan koneksi LLM (<code>llm.py</code>).</li>
            <li><b>Deterministic Tools:</b> 8 modul alat independen yang murni menggunakan library Scikit-Learn dan Pandas.</li>
            <li><b>Separation of Concerns:</b> Tidak ada kode alat yang mencemari logika orkestrasi pipeline.</li>
          </ul>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Slide ini memetakan seluruh repositori agar dewan penguji dapat melihat dengan jelas batas tanggung jawab setiap modul. Kami memetakan seluruh repositori agar penguji dapat melihat dengan jelas batas tanggung jawab setiap direktori dan alur ketergantungan antar-file. Setiap file memiliki tujuan spesifik yang terukur.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 29: FILE DEEP DIVE 1 - ENGINE & STATE
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 29: FILE DEEP DIVE 1 -->
    <section class="slide" data-slide="29">
      <div class="slide-badge">BEDAH FILE: ENGINE & STATE</div>
      <h2 class="slide-title">Bedah File: main.py, core/state.py, & core/llm.py</h2>
      <p class="slide-subtitle">Pondasi kontrol eksekusi, manajemen memori state tunggal, dan disiplin pemanggilan LLM</p>
      
      <div class="grid-3">
        <div class="glass-card" style="border-top: 3px solid var(--accent-gold);">
          <div style="font-family: var(--font-mono); font-size: 0.82rem; color: var(--accent-gold); font-weight: 700; margin-bottom: 6px;">main.py</div>
          <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: #FFF; margin-bottom: 6px;">Dispatcher CLI</h3>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.45; margin-bottom: 10px;">Menggunakan argparse untuk menangani subperintah <code>train</code> dan <code>predict</code>. Menghubungkan input pengguna ke pipeline inti dan mengembalikan kode status exit yang tepat.</p>
          <div style="background: rgba(0,0,0,0.5); padding: 8px; border-radius: 6px; font-family: var(--font-mono); font-size: 0.72rem; color: #FFF4E0;">
            sub = parser.add_subparsers(...)<br>train_p = sub.add_parser("train")<br>pred_p = sub.add_parser("predict")
          </div>
        </div>

        <div class="glass-card" style="border-top: 3px solid var(--agent-wrangler);">
          <div style="font-family: var(--font-mono); font-size: 0.82rem; color: var(--agent-wrangler); font-weight: 700; margin-bottom: 6px;">core/state.py</div>
          <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: #FFF; margin-bottom: 6px;">Blackboard SSOT</h3>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.45; margin-bottom: 10px;">Mendefinisikan <code>@dataclass SharedState</code> sebagai satu-satunya wadah memori sesi. Tidak ada variabel global; seluruh data sesi dapat diserialisasikan ke <code>state.json</code>.</p>
          <div style="background: rgba(0,0,0,0.5); padding: 8px; border-radius: 6px; font-family: var(--font-mono); font-size: 0.72rem; color: #FFF4E0;">
            @dataclass<br>class SharedState:<br>&nbsp;&nbsp;framing: Dict[str, Any]<br>&nbsp;&nbsp;model_eval: Dict[str, Any]
          </div>
        </div>

        <div class="glass-card" style="border-top: 3px solid var(--agent-guardian);">
          <div style="font-family: var(--font-mono); font-size: 0.82rem; color: var(--agent-guardian); font-weight: 700; margin-bottom: 6px;">core/llm.py</div>
          <h3 style="font-family: var(--font-heading); font-size: 1.05rem; color: #FFF; margin-bottom: 6px;">Gateway Gemini & Log</h3>
          <p style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.45; margin-bottom: 10px;">Mengisolasi API key via <code>.env</code> lokal, memaksa format JSON valid, melakukan retry maksimal 2x, dan mencatat jejak forensik ke <code>llm_log.jsonl</code>.</p>
          <div style="background: rgba(0,0,0,0.5); padding: 8px; border-radius: 6px; font-family: var(--font-mono); font-size: 0.72rem; color: #FFF4E0;">
            client = GeminiClient()<br>resp = client.call_json(...)<br>log_forensic_entry(...)
          </div>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Ketiga file ini adalah pondasi sistem. main.py mengontrol alur eksekusi, state.py menjaga memori bersama tanpa perdebatan tak tentu arah, dan llm.py menjamin setiap prompt dan response tercatat secara forensik.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 30: FILE DEEP DIVE 2 - DETERMINISTIC TOOLS
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 30: FILE DEEP DIVE 2 -->
    <section class="slide" data-slide="30">
      <div class="slide-badge">BEDAH FILE: TOOLS DETERMINISTIC</div>
      <h2 class="slide-title">Bedah File: profiling, cleaning, leakage, modeling, plotting</h2>
      <p class="slide-subtitle">Pemisahan tegas: Seluruh komputasi numerik dikerjakan oleh pustaka Python standar di core/tools/</p>
      
      <div class="grid-5" style="margin-bottom: 16px;">
        <div class="glass-card">
          <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--accent-gold); font-weight: 700;">profiling.py</div>
          <div style="font-size: 0.85rem; font-weight: 700; color: #FFF; margin: 4px 0;">Statistik Dasar</div>
          <div style="font-size: 0.78rem; color: var(--text-muted); line-height: 1.35;">Menghitung missing values, kurtosis, skewness, dan korelasi numerik via Pandas murni.</div>
        </div>
        <div class="glass-card">
          <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--danger); font-weight: 700;">leakage.py</div>
          <div style="font-size: 0.85rem; font-weight: 700; color: #FFF; margin: 4px 0;">Scan Bocor</div>
          <div style="font-size: 0.78rem; color: var(--text-muted); line-height: 1.35;">Memindai korelasi |r| >= 0.90 dan rasio pemetaan 1:1 terhadap label target.</div>
        </div>
        <div class="glass-card">
          <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--agent-wrangler); font-weight: 700;">cleaning.py</div>
          <div style="font-size: 0.85rem; font-weight: 700; color: #FFF; margin: 4px 0;">Sanitasi Fitur</div>
          <div style="font-size: 0.78rem; color: var(--text-muted); line-height: 1.35;">Membangun ColumnTransformer higienis dengan fit-in-fold dan drop identifier (>95%).</div>
        </div>
        <div class="glass-card">
          <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--agent-guardian); font-weight: 700;">modeling.py</div>
          <div style="font-size: 0.85rem; font-weight: 700; color: #FFF; margin: 4px 0;">5-Fold CV</div>
          <div style="font-size: 0.78rem; color: var(--text-muted); line-height: 1.35;">Melatih Baseline Dummy, kandidat Linear vs Ensemble, dan ukur gap overfit.</div>
        </div>
        <div class="glass-card">
          <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--agent-storyteller); font-weight: 700;">plotting.py</div>
          <div style="font-size: 0.85rem; font-weight: 700; color: #FFF; margin: 4px 0;">Render Plot</div>
          <div style="font-size: 0.78rem; color: var(--text-muted); line-height: 1.35;">Mengekstrak koefisien nyata dan merender 4 berkas PNG publikasi resolusi tajam.</div>
        </div>
      </div>

      <div class="glass-card" style="display: flex; align-items: center; justify-content: space-between;">
        <div style="font-size: 0.85rem; color: var(--text-muted);">
          <b>Kepatuhan Prinsip 'Python Mengerjakan':</b> Kelima modul di atas tidak memiliki dependensi terhadap API LLM. Seluruh perhitungan matematis dijalankan langsung oleh CPU lokal pengguna secara cepat dan dapat direproduksi.
        </div>
      </div>
      <div class="notes-data" style="display:none;">Kelima tool ini menjamin prinsip 'Python Mengerjakan'. Tidak ada komputasi yang diserahkan ke memori LLM. Seluruh angka berasal dari Scikit-Learn, Pandas, dan NumPy.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 31: FILE DEEP DIVE 3 - PRODUCTION & UI
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 31: FILE DEEP DIVE 3 -->
    <section class="slide" data-slide="31">
      <div class="slide-badge">BEDAH FILE: PRODUKSI & UI</div>
      <h2 class="slide-title">Bedah File: predict.py, notebook.py, session_payload.py, & app.py</h2>
      <p class="slide-subtitle">Menyulap hasil riset menjadi artefak produksi yang mandiri, tervalidasi, dan interaktif</p>
      
      <div class="grid-4" style="margin-bottom: 16px;">
        <div class="glass-card">
          <div style="font-family: var(--font-mono); font-size: 0.78rem; color: var(--accent-gold); font-weight: 700; margin-bottom: 4px;">predict.py</div>
          <div style="font-size: 0.95rem; font-weight: 700; color: #FFF; margin-bottom: 4px;">Inferensi Mandiri</div>
          <div style="font-size: 0.8rem; color: var(--text-muted); line-height: 1.4;">Memuat model.joblib, memvalidasi schema.json, dan menolak tegas kolom hilang sesuai standar validasi input produksi.</div>
        </div>
        <div class="glass-card">
          <div style="font-family: var(--font-mono); font-size: 0.78rem; color: var(--agent-builder); font-weight: 700; margin-bottom: 4px;">notebook.py</div>
          <div style="font-size: 0.95rem; font-weight: 700; color: #FFF; margin-bottom: 4px;">Replay Nbclient</div>
          <div style="font-size: 0.8rem; color: var(--text-muted); line-height: 1.4;">Merakit sel jupyter bersih via nbformat dan memverifikasi kelulusan eksekusi headless via nbclient.</div>
        </div>
        <div class="glass-card">
          <div style="font-family: var(--font-mono); font-size: 0.78rem; color: var(--agent-wrangler); font-weight: 700; margin-bottom: 4px;">session_payload.py</div>
          <div style="font-size: 0.95rem; font-weight: 700; color: #FFF; margin-bottom: 4px;">Adapter UI Arena</div>
          <div style="font-size: 0.8rem; color: var(--text-muted); line-height: 1.4;">Membaca state.json dan merakit payload terpadu untuk disajikan ke panggung visual Streamlit.</div>
        </div>
        <div class="glass-card">
          <div style="font-family: var(--font-mono); font-size: 0.78rem; color: var(--agent-storyteller); font-weight: 700; margin-bottom: 4px;">app.py & index.html</div>
          <div style="font-size: 0.95rem; font-weight: 700; color: #FFF; margin-bottom: 4px;">Streamlit Arena</div>
          <div style="font-size: 0.8rem; color: var(--text-muted); line-height: 1.4;">Antarmuka web interaktif bertema Dark Chocolate & Honey Gold dengan form prediksi dinamis.</div>
        </div>
      </div>

      <div class="terminal-box">
        <div class="terminal-header">
          <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
          <div class="terminal-title">Integrasi Hulu ke Hilir: Dari Pelatihan ke Antarmuka</div>
        </div>
        <div class="terminal-body"><span class="c-comment"># 1. Pelatihan menghasilkan artefak: outputs/run_id/state.json, model.joblib, schema.json</span>
<span class="c-comment"># 2. session_payload.py membaca state.json -> disajikan di app.py (Streamlit Arena)</span>
<span class="c-comment"># 3. Form prediksi di app.py membaca schema.json -> memanggil predict.py secara mandiri</span></div>
      </div>
      <div class="notes-data" style="display:none;">Inilah jembatan dari eksperimen ke dunia nyata. predict.py melayani inferensi produksi, notebook.py menjamin reproduktibilitas ilmiah, dan app.py memberikan pengalaman interaktif bagi pemangku kepentingan bisnis.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 32: AUDIT 9 DOD CRITERIA
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 32: AUDIT 9 DOD -->
    <section class="slide" data-slide="32">
      <div class="slide-badge" style="color: var(--success); border-color: rgba(141,178,85,0.4); background: rgba(141,178,85,0.1);">MATRIKS EVALUASI KELAYAKAN SISTEM</div>
      <h2 class="slide-title">Matriks Evaluasi 9 Kriteria Kelulusan & Definisi Selesai</h2>
      <p class="slide-subtitle">Bukti pemenuhan 100% seluruh kriteria penilaian resmi evaluasi dewan penguji</p>
      
      <div class="grid-3" style="gap: 12px;">
        <div class="kriteria-card">
          <span class="kriteria-badge pass">LULUS</span>
          <div>
            <div class="kriteria-title">Kriteria 1: CLI Training Berjalan Penuh</div>
            <div class="kriteria-desc">Terbukti tuntas pada 3 dataset: Titanic, Insurance, dan Telco Churn tanpa intervensi manual.</div>
          </div>
        </div>
        <div class="kriteria-card">
          <span class="kriteria-badge pass">LULUS</span>
          <div>
            <div class="kriteria-title">Kriteria 2: Bebas Data Hardcode</div>
            <div class="kriteria-desc">Dataset berbeda menghasilkan keputusan, pilihan model champion, dan metrik yang berbeda.</div>
          </div>
        </div>
        <div class="kriteria-card">
          <span class="kriteria-badge pass">LULUS</span>
          <div>
            <div class="kriteria-title">Kriteria 3: Notebook Tervalidasi Nbclient</div>
            <div class="kriteria-desc">notebook.ipynb dijalankan ulang secara headless tanpa runtime error; metrik cocok.</div>
          </div>
        </div>
        <div class="kriteria-card">
          <span class="kriteria-badge pass">LULUS</span>
          <div>
            <div class="kriteria-title">Kriteria 4: Bukti Nyata API LLM</div>
            <div class="kriteria-desc">Setiap prompt, latensi ms, dan respons tercatat forensik di outputs/&lt;run_id&gt;/llm_log.jsonl.</div>
          </div>
        </div>
        <div class="kriteria-card">
          <span class="kriteria-badge pass">LULUS</span>
          <div>
            <div class="kriteria-title">Kriteria 5: Gagal Harus Terlihat</div>
            <div class="kriteria-desc">Jika API LLM offline, sistem berhenti seketika dengan pesan transparan (SystemExit).</div>
          </div>
        </div>
        <div class="kriteria-card">
          <span class="kriteria-badge pass">LULUS</span>
          <div>
            <div class="kriteria-title">Kriteria 6: Metrik Murni dari Python</div>
            <div class="kriteria-desc">Tidak ada angka di laporan yang tidak berasal dari eksekusi Scikit-Learn lokal.</div>
          </div>
        </div>
        <div class="kriteria-card">
          <span class="kriteria-badge pass">LULUS</span>
          <div>
            <div class="kriteria-title">Kriteria 7: Pytest Suite 6/6 Lulus</div>
            <div class="kriteria-desc">Menguji profiling, mock LLM flow, planted leakage, dan penolakan kolom hilang.</div>
          </div>
        </div>
        <div class="kriteria-card">
          <span class="kriteria-badge pass">LULUS</span>
          <div>
            <div class="kriteria-title">Kriteria 8: Inferensi Mandiri & Penolakan</div>
            <div class="kriteria-desc">Mode predict memuat model.joblib dan menolak input tidak lengkap via ValueError.</div>
          </div>
        </div>
        <div class="kriteria-card">
          <span class="kriteria-badge ready">SIAP UJI</span>
          <div>
            <div class="kriteria-title">Kriteria 9: Penguasaan Materi Repositori</div>
            <div class="kriteria-desc">Presenter siap membedah setiap baris kode, arsitektur modul, dan keputusan teknis agen.</div>
          </div>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Tabel ini merangkum pembuktian kepatuhan terhadap seluruh 9 kriteria kelulusan resmi. Kami tidak meminta kelulusan atas dasar janji, melainkan atas dasar bukti eksekusi nyata yang tersimpan di dalam berkas log, test suite, dan artefak model.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 33: STREAMLIT SHADOW ARENA
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 33: STREAMLIT ARENA -->
    <section class="slide" data-slide="33">
      <div class="slide-badge">INTEGRASI STREAMLIT ARENA</div>
      <h2 class="slide-title">Shadow Arena: Visualisasi & Kontrol Interaktif</h2>
      <p class="slide-subtitle">Antarmuka web bertema Dark Chocolate & Honey Amber yang selaras sempurna dengan presentasi</p>
      
      <div class="grid-2">
        <div class="glass-card" style="display: flex; flex-direction: column; justify-content: space-around;">
          <div>
            <h3 style="font-family: var(--font-heading); font-size: 1.15rem; color: var(--accent-gold); margin-bottom: 10px;">Fitur Interaktif Shadow Arena:</h3>
            <ul class="bullet-list">
              <li><b>Panggung Visual Melingkar:</b> Menampilkan 5 agen dengan avatar dan status aktif secara responsif berbasis <code>index.html</code>.</li>
              <li><b>Penjelajah Sesi Riset:</b> Membaca seluruh riwayat eksperimen di folder <code>outputs/</code> berbasis SSOT <code>state.json</code>.</li>
              <li><b>Unduh Notebook Tervalidasi:</b> Tombol <code>st.download_button</code> untuk mengunduh berkas <code>notebook.ipynb</code> siap pakai.</li>
              <li><b>Formulir Prediksi Dinamis:</b> Membaca <code>schema.json</code> dan merakit widget input numerik/kategori secara otomatis.</li>
              <li><b>Latih Data Baru:</b> Form upload CSV untuk meluncurkan pipeline 5 agen pada dataset baru secara langsung.</li>
            </ul>
          </div>
        </div>

        <div class="terminal-box">
          <div class="terminal-header">
            <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="terminal-title">Menjalankan Arena Interaktif Lokal</div>
          </div>
          <div class="terminal-body">> streamlit run app.py
  You can now view your Streamlit app in your browser.
  Local URL: <span class="c-str">http://localhost:8501</span>

<span class="c-comment"># Komponen UI Terintegrasi:</span>
<span class="c-keyword">1. Circular 5-Agent Stage</span> (index.html)
<span class="c-keyword">2. SSOT Session Browser</span> (session_payload.py)
<span class="c-keyword">3. Dynamic Predict Form</span> (schema.json auto-build)
<span class="c-keyword">4. Validated Notebook Download</span> (notebook.ipynb)</div>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Aplikasi Streamlit Shadow Arena kami mengusung tema Dark Chocolate dan Madu Emas yang serasi dengan slide presentasi ini. Arena ini menghubungkan output state.json langsung ke antarmuka pengguna tanpa perantara tambahan.</div>
    </section>
""")

    # -------------------------------------------------------------
    # SLIDE 34: CONCLUSION & LIVE DEMO
    # -------------------------------------------------------------
    slides.append("""    <!-- SLIDE 34: CONCLUSION -->
    <section class="slide" data-slide="34">
      <div class="hero-container" style="justify-content: flex-start; padding-top: 8px;">
        <div class="hero-badge-glow">KESIMPULAN & SESI TANYA JAWAB</div>
        <h1 class="hero-h1" style="font-size: 2.5rem; margin-bottom: 8px;">Sains Data yang Jujur, Tangguh, & Auditable</h1>
        <p class="hero-lead" style="font-size: 1.05rem; margin-bottom: 14px; max-width: 920px;">Platform multi-agen machine learning otonom pertama dengan jaminan zero target leakage, komputasi deterministik Scikit-Learn, dan notebook yang tervalidasi 100%.</p>
        
        <div class="hero-pill-grid" style="margin-bottom: 14px; gap: 8px;">
          <div class="hero-pill">🤖 <b>5 Agen Otonom:</b> Problem Framer s.d. Notebook Builder</div>
          <div class="hero-pill">🔒 <b>Bebas Data Leakage:</b> Penapisan pra-split deterministik mutlak</div>
          <div class="hero-pill">⚙️ <b>Zero Hallucination:</b> Komputasi Python Scikit-Learn murni</div>
          <div class="hero-pill">🧪 <b>Siap Uji Langsung:</b> 6/6 Pytest & inferensi mandiri data baru</div>
        </div>

        <div class="terminal-box" style="max-width: 860px; width: 100%; margin-bottom: 14px;">
          <div class="terminal-header">
            <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
            <div class="terminal-title">bash — Live Demo 5 Agen Otonom SHADOW di Hadapan Dewan Penguji</div>
          </div>
          <div class="terminal-body"><span class="c-comment"># 1. Jalankan 5 Agen Otonom pada File CSV Baru Apa Pun dari Dewan Penguji:</span>
> python main.py train data/dataset_penguji.csv
<span class="c-comment"># Alur Maju: [Framer] -> [Wrangler] -> [Guardian] -> [Storyteller] -> [Builder]</span>

<span class="c-comment"># 2. Uji Mode Prediksi Mandiri (Standalone Inference) pada Model yang Baru Dilatih:</span>
> python main.py predict --run outputs/run_latest --input <span class="c-str">'{"fitur_A": 10, "fitur_B": "kategori"}'</span>

<span class="c-comment"># 3. Verifikasi Seluruh Suite Pengujian Kualitas Sistem:</span>
> python -m pytest tests/ -v</div>
        </div>

        <div class="hero-meta-footer" style="padding-top: 10px;">
          <div style="font-size: 1.05rem; color: var(--accent-gold); font-weight: 700;">
            🎓 Sesi Tanya Jawab & Live Demonstration Resmi Dibuka
          </div>
        </div>
      </div>
      <div class="notes-data" style="display:none;">Terima kasih atas perhatian Bapak dan Ibu Dewan Penguji. Sistem SHADOW Multi-Agent ini siap diuji secara langsung pada file CSV baru apa pun yang diberikan oleh dewan penguji hari ini. Kelima agen akan bekerja secara otonom dari perumusan target hingga penerbitan notebook tervalidasi.</div>
    </section>
""")

    return slides

if __name__ == "__main__":
    html_content = generate_slides_html()
    assert html_content.count("$") == 0, "Ada tanda dollar di berkas HTML!"
    OUTPUT_FILE.write_text(html_content, encoding="utf-8")
    print(f"BERHASIL: Menghasilkan 34 Slide HTML Masterclass di {OUTPUT_FILE}")
    print(f"Total Karakter: {len(html_content)}")
