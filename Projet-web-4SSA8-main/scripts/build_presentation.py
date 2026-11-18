#!/usr/bin/env python3
"""Validation 1 PPTX — max 12 slides, speaker notes + timing, one MS per member."""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

OUT = Path(__file__).resolve().parents[1] / "Documentation" / "Presentation" / "Validation1-JobBoard.pptx"


def style_title(p, text, size=28):
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)


def add_slide(prs, title, bullets, notes, timing):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    tb = slide.shapes.add_textbox(Inches(0.4), Inches(0.25), Inches(9.2), Inches(0.7))
    style_title(tb.text_frame.paragraphs[0], title, 26)
    body = slide.shapes.add_textbox(Inches(0.5), Inches(1.1), Inches(9), Inches(5.8))
    tf = body.text_frame
    tf.word_wrap = True
    for i, line in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(18)
        p.space_after = Pt(10)
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = f"[Timing: {timing}]\nSpeaker: {notes}"
    return slide


def main():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # 12 slides max — 6 speakers
    add_slide(
        prs,
        "1. JobBoard — Validation 1",
        [
            "ESPRIT AWD 2026-2027 · ~10 minutes",
            "Équipe (6): Aziz · Rayen · Maryem · Ezzedine · Dhia · Samer",
            "Objectif: design microservices + squelettes (pas tout le métier)",
            "Réfs: Symfony JobBoard + Spring awd-monolith / awd_db",
        ],
        "Aziz ouvre: plan (sujet → split → 5 MS → plateforme Samer → questions).",
        "0:00–0:40",
    )
    add_slide(
        prs,
        "2. Problème & acteurs (E1)",
        [
            "Problème: monolithes (base unique, process unique, 1 port)",
            "Acteurs: Candidat · Recruteur · Admin · Notification",
            "15 user stories (US-01…US-15) mappées aux MS",
            "Périmètre réaliste: V1 = conception + squelettes",
        ],
        "Aziz: problème concret + acteurs + renvoi US dans 00-sujet.",
        "0:40–1:20",
    )
    add_slide(
        prs,
        "3. Domaine DDD & Context Map",
        [
            "Core: Candidature + Catalogue",
            "Support: Identité candidat + Entretien",
            "Generic: Notification + Keycloak",
            "Diagramme: Documentation/Diagrams/context-map.svg",
        ],
        "Maryem: expliquer core vs support vs generic et Customer/Supplier vs events.",
        "1:30–2:20",
    )
    add_slide(
        prs,
        "4. Découpage (rejets inclus)",
        [
            "5 MS = capacités métier — PAS 1 service / table",
            "Address∈candidate · Category∈job",
            "Rejeté: DB partagée · notif sync dans apply",
        ],
        "Rayen: table responsabilités + alternatives rejetées (E2).",
        "2:20–3:10",
    )
    add_slide(
        prs,
        "5. ms-candidate — Aziz Mehrez",
        [
            "Port 8081 · MySQL candidate_db :3307",
            "Candidate + Address · API /api/candidates",
            "Appelé en Feign par ms-application",
        ],
        "AZIZ présente SON service: entités, DB, API, failure si down.",
        "3:10–4:00",
    )
    add_slide(
        prs,
        "6. ms-job — Rayen Sboui",
        [
            "Port 8082 · MySQL job_db :3308",
            "Job + Category · PATCH availability",
            "Event: JobAvailabilityChanged",
        ],
        "RAYEN: responsabilités, ce qu'il ne fait PAS, event async.",
        "4:00–4:50",
    )
    add_slide(
        prs,
        "7. ms-application — Maryem Slatni",
        [
            "Port 8083 · PostgreSQL :5433",
            "IDs seulement (pas de FK cross-DB)",
            "Feign sync + ApplicationCreated async",
            "CB Resilience4j → 503 si dépendance down",
        ],
        "MARYEM: cœur métier, sync vs async, plan de panne.",
        "4:50–5:50",
    )
    add_slide(
        prs,
        "8. ms-interview — Ezzedine Zouiten",
        [
            "Port 8084 · MongoDB interview_db",
            "Document Interview · applicationId logique",
            "Events InterviewScheduled / Cancelled",
        ],
        "EZZEDINE: pourquoi Mongo, Feign vers application, events.",
        "5:50–6:40",
    )
    add_slide(
        prs,
        "9. ms-notification — Dhia Jbali (avancé)",
        [
            "Port 8085 · Python FastAPI + RabbitMQ",
            "Consomme events · pas d'appel sync métier",
            "LLM optionnel · fallback template",
        ],
        "DHIA: pourquoi avancé/polyglotte, idempotence eventId.",
        "6:20–7:00",
    )
    add_slide(
        prs,
        "10. Plateforme — Samer (E4)",
        [
            "API Gateway :8080 · Eureka :8761 · Config :8888",
            "Keycloak :8180 · RabbitMQ · Docker Compose",
            "Entrée unique web/mobile · discovery · IAM JWT",
            "Diagramme: Documentation/Diagrams/architecture.svg",
        ],
        "SAMER: stack imposée, ports, pourquoi Gateway+Eureka vs monolithe :8080.",
        "7:00–8:00",
    )
    add_slide(
        prs,
        "11. Données & communication (E3)",
        [
            "1 DB / service · jamais de FK cross-service",
            "Sync Feign = invariants · Async events = mails",
            "Timeout / Retry / CB Resilience4j / cohérence éventuelle",
        ],
        "Maryem + Dhia: matrice + events (30s chacun).",
        "8:00–8:50",
    )
    add_slide(
        prs,
        "12. Repo, plan & questions (E5/E6)",
        [
            "Backend/ Frontend/ Documentation/ · README · Issues",
            "Chaque membre commit · Samer = compose/gateway",
            "Questions ?",
        ],
        "Tous prêts (QA_PREP + MEMBER_BRIEFS). Temps total ~10 min.",
        "8:50–10:00",
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    print(f"Wrote {OUT} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
