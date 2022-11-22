import { defineConfig } from "astro/config";
import Unocss from "unocss/astro";
import { presetUno } from "unocss";

// https://astro.build/config
import react from "@astrojs/react";

// https://astro.build/config
export default defineConfig({
  integrations: [
    react(),
    Unocss({
      presets: [presetUno()],
    }),
  ],
});
