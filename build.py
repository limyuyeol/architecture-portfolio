"""Build a dependency-free, GitHub Pages-compatible HTML portfolio.

Edit content.json, then run: python build.py
"""
import json
import pathlib
from html import escape

ROOT = pathlib.Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))
ASSETS = {a['asset'][:-5]: a for a in json.loads((ROOT / 'sources/asset-sources.json').read_text(encoding='utf-8'))}
PROJECTS = DATA['projects']
FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' fill='%23191919'/%3E%3Cpath d='M16 14v36h32M28 14v24h20' fill='none' stroke='%23f35c35' stroke-width='6'/%3E%3C/svg%3E"


def e(value):
    return escape(str(value), quote=True)


def image(key, caption, prefix='', large=False, eager=False, cls=''):
    asset = ASSETS[key]
    src = f'{prefix}assets/images/{key}.webp'
    thumb = f'{prefix}assets/images/{key}-thumb.webp'
    return f'<img class="{cls}" src="{src if large else thumb}" alt="{e(caption)}" width="{asset["width"]}" height="{asset["height"]}" loading="{"eager" if eager else "lazy"}" decoding="async"' + (' fetchpriority="high"' if eager else '') + '>'


def header(prefix='', current=''):
    return f'''<a class="skip-link" href="#main">본문으로 건너뛰기</a>
<header class="site-header"><a class="brand" href="{prefix}index.html" aria-label="임유열 포트폴리오 홈"><span class="brand-mark" aria-hidden="true">LY</span><span>임유열 <span class="brand-sub">ARCHITECTURE PORTFOLIO</span></span></a>
<nav aria-label="주 메뉴"><a href="{prefix}index.html#archive" {'aria-current="page"' if current == 'archive' else ''}>학년별 기록</a><a href="{prefix}index.html#about">소개</a><a class="github-link" href="https://github.com/limyuyeol" target="_blank" rel="noopener noreferrer">GitHub <span class="external-symbol" aria-hidden="true">↗</span></a></nav></header>'''


def footer(prefix=''):
    return f'''<footer class="site-footer"><div><a class="footer-name" href="{prefix}index.html">LIM YU YEOL.</a><p>관찰하고, 그리며, 만들어 온 공간의 기록.</p></div><div class="footer-meta"><span>ARCHITECTURE · SELECTED WORKS</span><a href="{prefix}index.html#archive">학년별 작업 보기</a><span>© 임유열 · 포트폴리오</span></div></footer>
<script src="{prefix}assets/site.js" defer></script>'''


def shell(title, description, body, prefix='', current=''):
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><title>{e(title)} · 임유열</title><meta name="description" content="{e(description)}"><meta property="og:title" content="{e(title)} · 임유열"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="website"><link rel="icon" type="image/svg+xml" href="{FAVICON}"><link rel="stylesheet" href="{prefix}assets/style.css"></head><body>{header(prefix, current)}{body}{footer(prefix)}</body></html>'''


def year_nav(active=None, prefix=''):
    items = []
    for year in DATA['years']:
        count = len([p for p in PROJECTS if p['grade'] == year['id']])
        detail = f'{count:02} WORKS · {year["period"]}' if count else 'COMING SOON'
        items.append(f'''<a class="year-link {'is-active' if active == year['id'] else ''}" href="{prefix}year-{year['id']}.html" {'aria-current="page"' if active == year['id'] else ''}><span class="year-number">0{year['id']}</span><span class="year-info"><strong>{year['id']}학년</strong><span>{year['en']}</span></span><span class="year-status">{detail}</span></a>''')
    return '<nav class="year-nav" aria-label="학년 선택">' + ''.join(items) + '</nav>'


def card(project, prefix='', index=None):
    return f'''<article class="project-card"><a href="{prefix}projects/{project['id']}.html"><div class="card-image">{image(project['cover'], project['title'] + ' 대표 이미지', prefix)}<span class="card-type">{project['category']}</span><span class="card-open">작품 보기</span></div><div class="card-meta"><span>{project['grade']}학년 {project['term']}학기 · {project['year']}</span><span>{'STUDY' if 'study' in project['id'] else 'PROJECT'}</span></div><h3>{e(project['title'])}</h3><p>{e(project['summary'])}</p></a></article>'''


def build_home():
    selected = [next(p for p in PROJECTS if p['id'] == pid) for pid in ['combine-art-center', 'chodo-restroom', 'capture-a-sound']]
    body = f'''<main id="main">
<section class="home-hero wrap" aria-labelledby="home-title"><div class="hero-topline"><span>SELECTED WORKS / 2021—2024</span><span>CHONNAM NATIONAL UNIVERSITY · ARCHITECTURAL ENGINEERING</span></div>
<div class="hero-layout"><div class="hero-copy"><p class="eyebrow"><span class="accent-rule"></span>공간을 통해 나를 이야기합니다</p><h1 id="home-title">설계로 시작한 생각,<br><span>공학으로 넓어진 시선.</span></h1><p class="hero-intro">{e(DATA['intro'])}</p><a class="solid-link" href="#archive">나의 작업 살펴보기 <span>01—04</span></a><div class="hero-credit"><strong>{e(DATA['name'])}</strong><span>{e(DATA['nameEn'])}<br>ARCHITECTURE PORTFOLIO</span></div></div>
<a class="hero-visual" href="projects/combine-art-center.html">{image('2-2-098', '양림동 COMBINE 아트센터 — 긴 처마와 외부공간 투시도', large=True, eager=True)}<span class="hero-image-label"><span><small>FEATURED PROJECT · 2학년 2학기</small><strong>COMBINE</strong></span><span class="image-caption">일상의 이야기를 잇다</span></span><span class="image-index">12 / SELECTED WORK</span></a></div>
<div class="hero-bottom"><span>DRAWING. MODEL. SPACE.</span><span>작은 선에서 시작해, 하나의 장소가 되기까지.</span><span class="orange">PORTFOLIO / 01</span></div></section>
<section class="archive-section wrap" id="archive" aria-labelledby="archive-title"><div class="section-heading"><div><p class="eyebrow">THE ACADEMIC ARCHIVE</p><h2 id="archive-title">배움이 쌓이는 순서</h2></div><p>학년을 선택해 학기별 작업과<br>설계 과정을 살펴보세요.</p></div>{year_nav()}</section>
<section class="selected-section wrap" aria-labelledby="selected-title"><div class="section-heading"><div><p class="eyebrow">SELECTED PROJECTS</p><h2 id="selected-title">생각이 담긴 공간들<span class="heading-dot">.</span></h2></div><span class="section-side">주거에서 공공공간까지</span></div><div class="selected-grid">{''.join(card(p) for p in selected)}</div></section>
<section class="about-section" id="about" aria-labelledby="about-title"><div class="wrap about-layout"><div class="about-title"><p class="eyebrow">ABOUT MY APPROACH</p><h2 id="about-title">손으로 익히고,<br>공간으로 답합니다.</h2><p>임유열 <span>/ LIM YU YEOL</span></p></div><div class="about-content"><p class="about-lead">건축을 배우며 관심을 두어 온 것은<br>사람의 일상과 장소에 담긴 이야기입니다.</p><p>1학년에는 선과 도면, 모형으로 건축의 기초를 익혔습니다. 2학년에는 주거와 상업공간을 거쳐, 양림동의 쉼터와 아트센터로 설계의 범위를 넓혔습니다. 이곳에는 완성된 결과와 함께 생각을 다듬어 온 과정도 담았습니다.</p><dl class="approach-list"><div><dt><span>01</span> 관찰하기</dt><dd>답사와 사례 분석에서 장소의 조건을 읽습니다.</dd></div><div><dt><span>02</span> 구체화하기</dt><dd>개념을 스케치와 평면·단면·입면으로 옮깁니다.</dd></div><div><dt><span>03</span> 만들어 보기</dt><dd>모형과 시각화로 공간의 관계를 확인합니다.</dd></div></dl></div></div></section>
</main>'''
    (ROOT / 'index.html').write_text(shell('공간을 통해 나를 이야기합니다', DATA['intro'], body), encoding='utf-8')


def build_year(year):
    count = len([p for p in PROJECTS if p['grade'] == year['id']])
    body = f'''<main id="main"><div class="wrap"><div class="breadcrumb"><a href="index.html">HOME</a><span>/</span><span>{year['id']}학년</span></div><section class="year-hero"><div><p class="eyebrow">YEAR 0{year['id']} / {year['en']}</p><h1>{year['id']}학년<span class="orange">.</span></h1></div><div class="year-description"><p class="year-period">{year['period']}</p><h2>{year['title']}</h2><p>{year['description']}</p></div></section>{year_nav(year['id'])}'''
    if count:
        body += '<nav class="semester-jump" aria-label="학기 바로가기">' + ''.join(f'<a href="#semester-{s["term"]}">{s["term"]}학기 <span>{s["course"]} · {s["year"]}</span></a>' for s in year['semesters']) + '</nav>'
        for semester in year['semesters']:
            works = [p for p in PROJECTS if p['grade'] == year['id'] and p['term'] == semester['term']]
            body += f'''<section class="semester-section" id="semester-{semester['term']}" aria-labelledby="term-{semester['term']}-title"><div class="semester-heading"><div class="semester-mark">0{semester['term']}<span>SEMESTER</span></div><div><p class="eyebrow">{semester['year']} · {semester['course']}</p><h2 id="term-{semester['term']}-title">{semester['title']}</h2><p>{semester['description']}</p></div><span class="work-count">{len(works):02} WORKS</span></div><div class="project-grid">{''.join(card(p) for p in works)}</div></section>'''
    else:
        body += f'''<section class="coming-soon"><span class="coming-index">0{year['id']}</span><div><p class="eyebrow">A CHAPTER YET TO BE SHARED</p><h2>{year['id']}학년의 기록을 준비하고 있습니다.</h2><p>{year['description']}</p><a class="text-link" href="year-2.html">2학년 작업 먼저 보기</a></div></section>'''
    body += '</div></main>'
    (ROOT / f'year-{year["id"]}.html').write_text(shell(f'{year["id"]}학년 · {year["title"]}', year['description'], body, current='archive'), encoding='utf-8')


def build_project(project):
    prefix = '../'
    body = f'''<main id="main"><div class="wrap"><nav class="breadcrumb" aria-label="현재 위치"><a href="../index.html">HOME</a><span>/</span><a href="../year-{project['grade']}.html">{project['grade']}학년</a><span>/</span><a href="../year-{project['grade']}.html#semester-{project['term']}">{project['term']}학기</a></nav><section class="project-heading"><p class="eyebrow">{project['en']}</p><h1>{e(project['title'])}</h1><p class="project-summary">{e(project['summary'])}</p><dl class="project-facts"><div><dt>YEAR / SEMESTER</dt><dd>{project['grade']}학년 {project['term']}학기 · {project['year']}</dd></div><div><dt>PROJECT TYPE</dt><dd>{project['category']}</dd></div><div><dt>CONTRIBUTION</dt><dd>{project['type']}</dd></div><div><dt>SITE / SUBJECT</dt><dd>{e(project['site'])}</dd></div></dl></section>
<figure class="project-cover">{image(project['cover'], project['title']+' 대표 이미지', prefix, large=True, eager=True)}<figcaption>{e(project['title'])} <span>{project['year']} / {project['grade']}학년 {project['term']}학기</span></figcaption></figure>
<section class="concept-section" aria-labelledby="concept-title"><div><p class="eyebrow">THE IDEA</p><h2 id="concept-title">생각의 출발점</h2></div><div><p class="concept-text">{e(project['concept'])}</p><ol class="process-list">{''.join(f'<li><span>0{i+1}</span><div><h3>{e(point[0])}</h3><p>{e(point[1])}</p></div></li>' for i,point in enumerate(project['points']))}</ol></div></section>
<section class="gallery-section" aria-labelledby="gallery-title"><div class="section-heading"><div><p class="eyebrow">PROCESS & OUTCOME</p><h2 id="gallery-title">과정과 결과</h2></div><p class="gallery-instruction">사진을 누르면 크게 볼 수 있습니다.</p></div><div class="gallery-grid">'''
    for idx, (key, caption) in enumerate(project['gallery']):
        asset = ASSETS[key]
        portrait = asset['height'] > asset['width'] * 1.4
        body += f'''<figure class="gallery-item {'portrait' if portrait else ''}"><button type="button" class="gallery-button" data-image="../assets/images/{key}.webp" data-caption="{e(caption)}" aria-label="{e(caption)} 크게 보기">{image(key, caption, prefix)}<span class="zoom-label" aria-hidden="true">확대 보기 +</span></button><figcaption><span>{idx+1:02}</span>{e(caption)}</figcaption></figure>'''
    body += '</div></section>'
    peers = [p for p in PROJECTS if p['grade'] == project['grade'] and p['id'] != project['id']]
    nextp = peers[0]
    idx = PROJECTS.index(project)
    if idx + 1 < len(PROJECTS) and PROJECTS[idx+1]['grade'] == project['grade']:
        nextp = PROJECTS[idx+1]
    body += f'''<nav class="project-end" aria-label="다른 작업 보기"><a href="../year-{project['grade']}.html#semester-{project['term']}"><small>BACK TO THE ARCHIVE</small><strong>{project['grade']}학년 작업 목록</strong></a><a href="{nextp['id']}.html"><small>EXPLORE ANOTHER PROJECT</small><strong>{e(nextp['title'])}</strong></a></nav></div></main>
<dialog class="lightbox" aria-label="작품 이미지 확대 보기"><div class="lightbox-top"><span id="lightbox-counter"></span><button type="button" class="lightbox-close" autofocus>닫기 <span aria-hidden="true">×</span></button></div><div class="lightbox-stage"><img id="lightbox-image" alt=""></div><div class="lightbox-bottom"><button type="button" class="lightbox-prev" aria-label="이전 이미지">이전</button><p id="lightbox-caption" aria-live="polite"></p><button type="button" class="lightbox-next" aria-label="다음 이미지">다음</button></div><a id="lightbox-original" target="_blank" rel="noopener noreferrer">원본 크기로 보기</a></dialog>'''
    (ROOT / 'projects' / f'{project["id"]}.html').write_text(shell(project['title'], project['summary'], body, prefix), encoding='utf-8')


def main():
    (ROOT / 'projects').mkdir(exist_ok=True)
    build_home()
    for year in DATA['years']:
        build_year(year)
    for project in PROJECTS:
        build_project(project)
    print(f'Built {5 + len(PROJECTS)} HTML pages.')


if __name__ == '__main__':
    main()
