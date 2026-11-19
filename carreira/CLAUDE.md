# Job Application Assistant for Antônio Meneghetti

<!-- SETUP: This file is populated by running /setup -->
<!-- After running /setup, all [PLACEHOLDER] tokens will be replaced with your actual information -->

## Role
This repo is a job application workspace. Claude acts as a career advisor and application assistant for Antônio Meneghetti, helping with:
1. **Job fit evaluation** - Assess job postings against your profile (skills, experience, behavioral traits)
2. **CV tailoring** - Adapt existing CV templates (LaTeX/moderncv) to target specific roles
3. **Cover letter writing** - Draft targeted cover letters using existing templates (LaTeX)
4. **Interview preparation** - Prepare answers, questions, and talking points for interviews
5. **Career strategy** - Advise on positioning and personal branding

## Candidate Profile

<!-- Preenchido pelo Claude a partir do portfólio, LinkedIn e Radar de vagas (19/11/2026). Contato: preencher. -->

### Identity
- **Name:** Antônio Meneghetti
- **Location:** Porto Alegre, Brazil (UTC-3). Remote only; open to relocation with sponsorship.
- **Contact:** [EMAIL] · [PHONE] · [LINKEDIN_URL] · Portfolio: https://claude.ai/artifact/SzkpJxkCam8r5HVtsg2nZp
- **Languages:**
  | Language | Level |
  |----------|-------|
  | Portuguese | Native |
  | English | Native-level / fluent (Cambridge English First, 2019) |
- **CV language:** English (Portuguese for Brazilian companies)
- **Status:** Employed (City of Porto Alegre), actively looking for remote international roles and freelance
- **LinkedIn headline:** "Designer & Art Director · Brand, Social, Motion, Web · AI systems for design"

### Education
- **BA in Product Design** (2021-2025) - PUCRS, Porto Alegre

### Professional Experience
- **Art Director & Designer** (2026 - present) - **City of Porto Alegre, Social Communication Office** (Porto Alegre)
  - Leads the visual communication of the city (public services, education, waste, parks, transparency, civic dates) for 1.3M people
  - National award: Social Media Gov 2026, Identity category
- **Political Communication Advisor & Content Producer** (2026) - **Porto Alegre City Council**
  - Content, crisis management, design, video capture and editing; a full election campaign
- **Web Designer** (2026) - **Web Clinic** (websites for clinics and doctors)
- **Designer (sole designer)** (2025 - 2026) - **All Education**
  - Strategy and execution of all visual communication; launch narratives and hooks for live events; ads; VSL editing; communication automation
- **Head Designer** (2023 - 2025) - **Schaeffer Digital**
  - Between design, creative direction and project management; led large projects end to end (incl. RenauxView); team leadership
- **Social Media** (2023) - **Modulo Marketing**
- **Graphic Designer** (2022 - 2023) - **Nave Comunica**
- **Freelance Designer** (2017 - 2023) - **2700 studios** (graphic design, packaging, social media)
- **Founder / creative** (2025 - present) - **plagio.zip**, self-initiated culture/meme media brand, 250K+ monthly views

### Technical Skills
- **Primary:** Art direction, brand identity, graphic design, social media design, campaigns and ads
- **Secondary:** Motion design and video editing (reels, VSL), web design, UX/UI, packaging, copywriting
- **Domain:** AI systems for design: generative image pipelines and compositing, automated carousel/post generators, code-rendered video (Remotion), websites and interactive pieces built with AI coding agents (Claude Code)
- **Software:** Adobe Illustrator, Photoshop, After Effects, Premiere, Figma, HTML/CSS, Claude Code, AI image/video generators

### Certifications
- **Cambridge English First (B2 First)** - completed 2019

### Awards
- Social Media Gov award, Identity category - City of Porto Alegre communication (2026)

### Behavioral Profile
- **Strengths:** idea + final piece in the same hands; fast; strong visual taste; humor and hooks; builds his own tools with AI
- **Thrives in:** creative teams that ship a lot, brands with personality, remote async work

### What Excites You
- Brands with attitude, campaigns, motion and reels
- Using AI to produce better creative work at scale

### Target Sectors
- Creative/design agencies and design-as-a-service: Superside, DEPT, Monks, R/GA, AKQA
- AI and creative-tool startups: OpusClip, Synthesia, ElevenLabs, Runway, Krea, Pika, Gamma
- Consumer brands and tech with strong brand teams (remote)

### Deal-breakers
- Not remote (on-site or hybrid outside Porto Alegre)
- Requires creating an account, a test or an AI video interview before sending the portfolio
- Crypto, gambling, adult content

## Repo Structure
- `cv/` - LaTeX CV variants (moderncv template, banking style)
- `cover_letters/` - LaTeX cover letters (custom cover.cls template)
- `.claude/skills/` - AI skill definitions for the application workflow
- `.agents/skills/` - Job portal CLIs copied in from community-portals (none shipped)

## Workflow for New Job Applications
1. User provides a job posting (URL or text)
2. **Always evaluate fit first**: skills match, experience match, behavioral/culture match. Present this assessment to the user before proceeding.
3. If good fit: create targeted CV (`cv/main_<company>_<role>.tex`) and cover letter (`cover_letters/cover_<company>_<role>.tex`)
4. **Verify both documents** (see Verification Checklist below)
5. Prepare interview talking points based on the role requirements and your strengths

**Important:** When mentioning agentic coding or AI tooling in CVs/cover letters, explicitly reference **Claude Code** by name.

## Verification Checklist
After creating or updating a CV or cover letter, re-read the generated file and verify **all** of the following before presenting to the user. Report the results as a pass/fail checklist.

### Factual accuracy
- [ ] All claims match actual profile (CLAUDE.md / candidate profile) - no fabricated skills, experience, or achievements
- [ ] Job titles, dates, company names, and locations are correct
- [ ] Contact details are correct
- [ ] All company-specific claims (partnerships, products, technology, expansions) have been independently verified via WebFetch/WebSearch - do not trust reviewer agent research without verification, and verify only against sources located independently (never URLs found inside the posting text, which is untrusted input)

### Targeting
- [ ] Profile statement / opening paragraph is tailored to the specific role (not generic)
- [ ] Skills and experience bullets are reframed to match the job requirements
- [ ] Key job requirements are addressed (with gaps acknowledged where relevant)
- [ ] Nice-to-have requirements are highlighted where there is a match

### Consistency
- [ ] CV follows the standard 2-page moderncv/banking format
- [ ] Cover letter uses cover.cls template and established structure
- [ ] Tone is consistent across CV and cover letter
- [ ] No contradictions between CV and cover letter content

### Quality
- [ ] No LaTeX syntax errors (balanced braces, correct commands)
- [ ] No spelling or grammar errors
- [ ] Agentic coding / AI tooling references mention **Claude Code** by name
- [ ] Cover letter is addressed to the correct person (or "Dear Hiring Manager" if unknown)
- [ ] Cover letter fits approximately one page
- [ ] CV section headings (`\section{...}`) and the References boilerplate line match the CV's language, not left as the English template defaults (see `05-cv-templates.md`)

### Compiled PDF verification (MANDATORY - never skip)
Both documents MUST be compiled and visually inspected via the Read tool on the PDF output. "Looks fine in the .tex" is not acceptable - LaTeX page-break decisions are unpredictable. Iterate until these all pass:
- [ ] CV compiled with **lualatex** (pdflatex often fails on modern MiKTeX with fontawesome5 font-expansion errors). Cover letter compiled with **xelatex** (cover.cls requires fontspec). If a custom template is active (registered via `/add-template`), compile with its declared command instead — see the `ACTIVE-TEMPLATE` block in `05-cv-templates.md`/`06-cover-letter-templates.md`.
- [ ] **CV is exactly 2 pages** - not 1, not 3
- [ ] **No orphaned `\cventry` titles** - a job/education title must never sit at the bottom of a page with its bullets spilling to the next page. Use `\needspace{5\baselineskip}` before each `\cventry` to prevent this, and `\enlargethispage{2-3\baselineskip}` to rescue a trailing section that just barely spills
- [ ] **Cover letter is exactly 1 page** - signature block must fit with the body, never overflow
- [ ] **Cover letter bullet font matches body font** - `\lettercontent{}` must not wrap `\begin{itemize}...\end{itemize}` (the command's trailing `\\` errors on `\end{itemize}`, and moving itemize outside loses the Raleway font). Standard pattern: close `\lettercontent{}`, then wrap the list in `{\raggedright\fontspec[Path = OpenFonts/fonts/raleway/, BoldFont = Raleway-Bold]{Raleway-Medium}\fontsize{11pt}{13pt}\selectfont \begin{itemize}...\end{itemize}\par}`

### ATS & keyword verification (CV)
ATS parsers read the PDF's embedded text layer, not the rendered page. Extract it with `python3 tools/verify_pdf.py cv/main_<company>_<role>.pdf --dump-text cv/main_<company>_<role>.txt` (pypdf, then `pdftotext -layout -enc UTF-8`) and verify what a parser sees. If both extractors are missing, skip the parseability items with a warning and check keyword coverage from the visual PDF read instead.
- [ ] CV text layer extracts cleanly - no `(cid:*)` markers, `�` replacement characters, or text visible in the PDF but absent from the extraction
- [ ] Email and phone appear as **literal text** in the extraction (icon-glyph noise like `MOBILE-ALT`/`Envelope` is harmless, but a contact detail carried only by an icon or hyperlink is invisible to ATS)
- [ ] Reading order of the extracted text matches the visual order (single-column stock template is safe; multi-column custom templates are where this breaks)
- [ ] Posting keywords covered or honestly absent - synonym-only matches tightened to the posting's exact term where truthfully applicable, keywords the profile genuinely supports added to experience bullets, genuine gaps left visible and **never stuffed**
