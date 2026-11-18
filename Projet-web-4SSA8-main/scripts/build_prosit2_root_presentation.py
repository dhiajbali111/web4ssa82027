#!/usr/bin/env python3
"""Prosit2/Presentation/Prosit2-JobBoard.pptx — max 12 slides + speaker notes."""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

OUT = Path(__file__).resolve().parents[1] / "Prosit2" / "Presentation" / "Prosit2-JobBoard.pptx"


def title_style(p, text, size=24):
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)


def add_slide(prs, title, bullets, notes):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    tb = slide.shapes.add_textbox(Inches(0.35), Inches(0.2), Inches(9.3), Inches(0.65))
    title_style(tb.text_frame.paragraphs[0], title, 22)
    body = slide.shapes.add_textbox(Inches(0.45), Inches(0.95), Inches(9.1), Inches(6.0))
    tf = body.text_frame
    tf.word_wrap = True
    for i, line in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(15)
        p.space_after = Pt(7)
    slide.notes_slide.notes_text_frame.text = notes
    return slide


def main():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    slides = [
        (
            "1. Prosit 2 — JobBoard monolithe → microservices",
            [
                "TalentConnect · ESPRIT AWD 2026-2027",
                "Source: Spring Boot 3.5.6 · awd-monolith · MySQL awd_db · :8080",
                "Livrable: dossier de conception + journal + slides (pas d'implémentation)",
                "Équipe (6): Aziz · Rayen · Maryem · Ezzedine · Dhia · Samer",
            ],
            "[0:00–0:40] Aziz ouvre: sujet design-only, annonce les 6 rôles.",
        ),
        (
            "2. Problématique",
            [
                "Comment passer du monolithe REST unique à des microservices",
                "scalables (recherche offres), polyglottes (Node / Python),",
                "sans monolithe distribué et sans notification synchrone bloquante ?",
            ],
            "[0:40–1:20] Aziz lit la question — tout le design y répond.",
        ),
        (
            "3. Acteurs — attentes & contraintes",
            [
                "Sami: ×50 recherche → 4× monolithe entier · restart = :8080 down",
                "Karim: 1 DB · rename job casse Application · delete lit table application",
                "Karim a proposé 1 MS/table — Sami refuse (latence, pannes)",
                "Inès: notif statut + créneau · SMTP sync = plus personne ne postule",
                "Leïla: équipes Node (entretiens) + Python (notif) · design collectif",
            ],
            "[1:20–2:10] Rayen lie chaque acteur à une décision (§3 dossier).",
        ),
        (
            "4. Diagnostic — preuves monolithe",
            [
                "pom.xml: Boot 3.5.6 · artifact awd-monolith · port 8080",
                "awd_db.sql: 5 tables + FK application→candidate/job",
                "JobService / CandidateService → ApplicationRepository → HTTP 409",
                "ApplicationService.create: @Transactional cross Candidate+Job",
                "OpenApiConfig: un contrat Swagger · stack Java-only",
                "Mail sync: ABSENT du code → ASSOMPTION scénario Inès",
            ],
            "[2:10–3:30] Rayen + Samer citent chemins si demandé.",
        ),
        (
            "5. Cartographie du domaine (DDD)",
            [
                "Cœur: Catalogue d'offres · Gestion des candidatures · Entretiens",
                "Support: Identité candidat (+ address)",
                "Générique: Notifications · Keycloak",
                "Address ≠ sous-domaine · Category ≠ sous-domaine",
            ],
            "[3:30–4:20] Maryem — découpage par capacité, pas par table.",
        ),
        (
            "6. Context Map",
            [
                "Offres / Candidat → Candidature: Customer/Supplier (Feign sync)",
                "Candidature → Entretien: Customer/Supplier",
                "Métiers → Notification: Published Language (events)",
                "Keycloak → tous: Conformist (JWT)",
                "Shared Kernel évité · ACL via DTO / mapping events",
            ],
            "[4:20–5:10] Maryem montre Diagrams/context-map.svg.",
        ),
        (
            "7. Microservices — 6 owners",
            [
                "ms-candidate (Java/MySQL) — Aziz",
                "ms-offer (Java/MySQL, scale seul) — Rayen",
                "ms-application (Java/PostgreSQL) — Maryem",
                "ms-interview (Node/Mongo) — Ezzedine",
                "ms-notification (Python, events) — Dhia",
                "Gateway / Eureka / Config / Keycloak — Samer",
            ],
            "[5:10–7:10] Chaque membre dit UNE phrase sur SON périmètre.",
        ),
        (
            "8. Communication sync / async",
            [
                "Sync Feign: candidat existe ? job available ?",
                "Async: ApplicationStatusChanged → notification (exigence Inès)",
                "Delete offre/candidat: Feign ms-application (plus de lecture table)",
                "SMTP / notif down: postuler reste possible",
                "Résilience: timeout, retry, circuit breaker, eventId idempotent",
            ],
            "[7:10–8:20] Dhia + Maryem: statut → mail = ASYNC obligatoire.",
        ),
        (
            "9. Architecture cible (plateforme)",
            [
                "Web / Mobile / Desktop → API Gateway",
                "Eureka + Config Server + Keycloak",
                "1 DB / service · RabbitMQ → ms-notification",
                "Diagramme: Prosit2/Diagrams/architecture.svg",
            ],
            "[8:20–9:30] Samer — légende sync vs async + ports.",
        ),
        (
            "10. Alternatives rejetées",
            [
                "1 service / table (Karim) → monolithe distribué",
                "Garder le monolithe → ne résout rien",
                "Extraire seulement la recherche → insuffisant",
                "Base partagée awd_db → incident rename Karim",
                "Communication 100 % sync → bloque Inès",
            ],
            "[9:30–10:20] Rayen — qualité des rejets = note.",
        ),
        (
            "11. Risques & roadmap strangler",
            [
                "Latence / pas d'ACID global / ops / monolithe distribué",
                "Mitigations: CB, sync ciblé, eventual consistency notifs",
                "Ordre: ms-offer → candidate → application → notification → interview",
                "Plateforme (Gateway/Eureka) en parallèle — Samer",
            ],
            "[10:20–11:30] Ezzedine + Samer.",
        ),
        (
            "12. Questions",
            [
                "Dossier: Prosit2/Dossier_Conception.md",
                "Journal: Prosit2/JOURNAL_EQUIPE.md (6 membres)",
                "Merci — l'équipe (6) répond",
            ],
            "[11:30–15:00] Tous prêts sur les 5 Q du README.",
        ),
    ]

    for t, b, n in slides:
        add_slide(prs, t, b, n)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
