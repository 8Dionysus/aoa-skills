# UI metadata and icon assets

The adapter export carries UI metadata through `agents/openai.yaml`.

## Added interface fields

Each skill now gets:

- `display_name`
- `short_description`
- `default_prompt`
- `icon_small`
- `icon_large`
- `brand_color`

## Asset strategy

The builder writes scope-based default SVG icons into each skill's `assets/` directory:

- core skills use a blue neutral icon
- risk skills use an amber warning-oriented icon
- project overlays use a violet layered icon

If canonical skills later gain bespoke assets, the builder can preserve them and avoid clobbering existing icon files.

## Override surface

Use `config/openai_skill_extensions.json` for per-skill UI overrides or MCP dependencies.
