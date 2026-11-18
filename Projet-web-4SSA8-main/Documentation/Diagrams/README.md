# Diagrammes JobBoard

Sources Mermaid (`.mmd`) à visualiser dans GitHub, VS Code (extension Mermaid), ou [mermaid.live](https://mermaid.live).

| Fichier | Contenu |
|---|---|
| `architecture.mmd` | Architecture globale |
| `context-map.mmd` | Context map DDD |
| `er-*.mmd` | Modèles de données par service |
| `sequence-apply.mmd` | Séquence candidature |
| `events-flow.mmd` | Flux d’événements RabbitMQ |

## Export PNG / SVG

Docker et `mmdc` n’étaient pas disponibles sur la machine de génération. Exporter ainsi :

```bash
# si Node est installé
npx -y @mermaid-js/mermaid-cli -i architecture.mmd -o architecture.svg
npx -y @mermaid-js/mermaid-cli -i architecture.mmd -o architecture.png
```

Ou coller le contenu sur https://mermaid.live → Actions → PNG/SVG.
