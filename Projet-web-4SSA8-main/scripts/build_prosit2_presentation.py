#!/usr/bin/env python3
"""Prosit 2 PPTX — max 12 slides (design dossier, no implementation demo)."""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

OUT = Path(__file__).resolve().parents[1] / "Documentation" / "Prosit2" / "Prosit2-JobBoard.pptx"


def style_title(p, text, size=26):
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0x1A, 0x36, 0x5D)


def add_slide(prs, title, bullets, notes):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    tb = slide.shapes.add_textbox(Inches(0.4), Inches(0.25), Inches(9.2), Inches(0.7))
    style_title(tb.text_frame.paragraphs[0], title, 24)
    body = slide.shapes.add_textbox(Inches(0.5), Inches(1.0), Inches(9), Inches(5.9))
    tf = body.text_frame
    tf.word_wrap = True
    for i, line in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(16)
        p.space_after = Pt(8)
    slide.notes_slide.notes_text_frame.text = notes
    return slide


def main():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    add_slide(
        prs,
        "1. Prosit 2 — JobBoard monolithe → microservices",
        [
            "TalentConnect · ESPRIT AWD 2026-2027",
            "Source: Spring Boot 3.5.6 · awd-monolith · MySQL awd_db · :8080",
            "Livrable: dossier de conception + journal + slides (pas d'implémentation)",
            "Équipe: Aziz · Rayen · Maryem · Ezzedine · Dhia",
        ],
        "Présenter le sujet et le format du prosit (design argumenté).",
    )
    add_slide(
        prs,
        "2. Problématique",
        [
            "Comment évoluer le monolithe REST unique vers des microservices",
            "scalables (recherche offres), polyglottes (Node / Python),",
            "sans monolithe distribué (pas 1 service/table, pas DB partagée,",
            "pas de notification synchrone qui bloque le dépôt de candidature) ?",
        ],
        "Lire la problématique telle quelle — c'est la question que le design répond.",
    )
    add_slide(
        prs,
        "3. Acteurs — attentes & contraintes",
        [
            "Sami: ×50 recherche → 4 copies du monolithe entier · restart = :8080 down",
            "Karim: 1 DB · rename job casse Application · delete lit table application",
            "Karim a proposé 1 MS/table — Sami s'y oppose (latence, pannes)",
            "Ines: notif statut + créneau entretien · SMTP sync = plus personne ne postule",
            "Leila: équipes Node (entretiens) + Python (notif) · design collectif argumenté",
        ],
        "Lier chaque acteur à une décision de design (slide suivante / dossier §3).",
    )
    add_slide(
        prs,
        "4. Diagnostic monolithe — preuves",
        [
            "1 artefact awd-monolith · Boot 3.5.6 · port 8080 · 3 packages",
            "awd_db: 5 tables + FK application→candidate/job",
            "CandidateService/JobService injectent ApplicationRepository → DELETE 409",
            "ApplicationService.create = @Transactional cross Candidate+Job",
            "OpenAPI unique · stack Java-only · mail sync = scénario (non dans le code)",
        ],
        "Citer chemins de fichiers du dossier §4 si l'examinateur demande la preuve.",
    )
    add_slide(
        prs,
        "5. Carte de domaine (DDD)",
        [
            "Cœur: Catalogue d'offres · Candidature",
            "Support: Identité candidat (+ address) · Entretiens",
            "Générique: Notifications · Keycloak IAM",
            "Address ≠ sous-domaine · Category ≠ sous-domaine",
        ],
        "Insister: découpage par capacité / BC, pas par table.",
    )
    add_slide(
        prs,
        "6. Context Map",
        [
            "Candidate / Job → Application: Customer/Supplier (Feign sync)",
            "Application → Interview: Customer/Supplier",
            "Métiers → Notification: Published Language (events RabbitMQ)",
            "Keycloak → tous: Conformist (JWT)",
            "Shared Kernel évité · ACL via DTO / mapping events",
        ],
        "Montrer context-map.svg si projecteur disponible.",
    )
    add_slide(
        prs,
        "7. Microservices retenus",
        [
            "ms-candidate (Java/MySQL): candidate + address",
            "ms-job (Java/MySQL): job + category — scalable seul (Sami)",
            "ms-application (Java/PostgreSQL): application (IDs only)",
            "ms-interview (Node/Mongo): créneaux",
            "ms-notification (Python): consomme events — jamais dans le chemin POST",
        ],
        "Rappeler redistribution des 5 tables et owners d'équipe.",
    )
    add_slide(
        prs,
        "8. Alternatives rejetées",
        [
            "A — 1 service / table (Karim): monolithe distribué",
            "B — Tout fusionner: pas de scale indépendant / pas de polyglotte",
            "C — 100 % sync: SMTP bloque Ines",
            "D — DB partagée awd_db: incident rename Karim",
            "E — Extraire seulement la recherche: ne règle pas ownership ni Node/Python",
        ],
        "La note dépend de la QUALITÉ de ces justifications.",
    )
    add_slide(
        prs,
        "9. Communication sync / async",
        [
            "Sync Feign: existe candidat ? job available ? (invariants)",
            "Async: ApplicationStatusChanged → notification (exigence Ines)",
            "Delete job/candidate: plus de lecture table application → Feign/API",
            "Si SMTP / notification down: postuler reste possible (cohérence éventuelle)",
            "Résilience: timeout, retry, circuit breaker, eventId idempotent",
        ],
        "Cas d'école: statut → mail = ASYNC obligatoire.",
    )
    add_slide(
        prs,
        "10. Architecture cible",
        [
            "Clients web / mobile / desktop → API Gateway",
            "Eureka + Config + Keycloak",
            "1 DB / service · RabbitMQ → ms-notification",
            "Diagramme: Documentation/Diagrams/architecture.svg",
        ],
        "Flèches: Feign = sync · RabbitMQ = async.",
    )
    add_slide(
        prs,
        "11. Trade-offs & risques",
        [
            "Latence réseau → timeouts / CB (pas de fantômes métier)",
            "Plus d'ACID global → sync ciblé + eventual consistency notifs",
            "Ops plus complexe → Compose pédagogique + health",
            "Risque monolithe distribué → frontières + journal d'équipe",
        ],
        "Assumer les risques — montrer les mitigations.",
    )
    add_slide(
        prs,
        "12. Questions",
        [
            "Journal: Documentation/Prosit2/JOURNAL_EQUIPE.md",
            "Dossier: Documentation/Prosit2/dossier-prosit2.md",
            "Merci — questions ?",
        ],
        "Préparer les 5 Q difficiles listées dans PROSIT2_AUDIT.md.",
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
