// Formulaire de demande professionnelle, rendu depuis le schéma Wix Forms.
// Aucun champ n'est nommé dans le code : les champs, libellés, choix, champs obligatoires et
// message de remerciement viennent du formulaire défini dans le tableau de bord Wix.
// Appels REST en visiteur anonyme (jeton OAuth du site), sur le modèle du kit Wix Headless :
// shared/rest/client.ts, forms/rest/forms.ts et forms/rest/submissions.ts.

const API = "https://www.wixapis.com";
const CLIENT_ID = "54772c88-ff94-47e9-aae5-997ba4660aa4";
const STORAGE_KEY = `wix-visitor-${CLIENT_ID}`;
const SUBMITTED_OK = new Set(["CONFIRMED", "PENDING", "PAYMENT_WAITING"]);
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const PHONE_PATTERN = /^\+[1-9]\d{1,14}$/;
const DIAL_CODES = { RE: "262", FR: "33", YT: "262", MU: "230" };

// ---- jeton visiteur (un par navigateur, conservé et rafraîchi) -----------------------------

let memory = null;
function loadTokens() {
  if (memory) return memory;
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) memory = JSON.parse(raw);
  } catch {
    /* stockage indisponible : nouveau visiteur */
  }
  return memory;
}
function saveTokens(t) {
  memory = t;
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(t));
  } catch {
    /* stockage indisponible */
  }
}
async function mint(body) {
  const res = await fetch(`${API}/oauth2/token`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ clientId: CLIENT_ID, ...body }),
  });
  if (!res.ok) throw new Error(`auth ${res.status}`);
  const d = await res.json();
  return { accessToken: d.access_token, refreshToken: d.refresh_token, expiresAt: Date.now() + d.expires_in * 1000 };
}
async function accessToken() {
  const t = loadTokens();
  if (t && t.expiresAt - 60000 > Date.now()) return t.accessToken;
  let fresh;
  if (t?.refreshToken) {
    try {
      fresh = await mint({ grantType: "refresh_token", refreshToken: t.refreshToken });
    } catch {
      /* nouveau visiteur ci-dessous */
    }
  }
  fresh ??= await mint({ grantType: "anonymous" });
  saveTokens(fresh);
  return fresh.accessToken;
}

class WixApiError extends Error {
  constructor(message, status, details) {
    super(message);
    this.status = status;
    this.details = details;
  }
}
async function wixRequest(path, { method = "POST", body } = {}) {
  const res = await fetch(API + path, {
    method,
    headers: { Authorization: await accessToken(), "Content-Type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  if (!res.ok) {
    let j = null;
    try { j = await res.json(); } catch { /* pas de JSON */ }
    throw new WixApiError(j?.message || `${method} ${path} (${res.status})`, res.status, j?.details);
  }
  return res.status === 204 ? null : res.json();
}

// ---- lecture du schéma ----------------------------------------------------------------------

const INPUT_BLOCK = { STRING: "stringOptions", NUMBER: "numberOptions", BOOLEAN: "booleanOptions", ARRAY: "arrayOptions" };

function richToText(rich) {
  if (!rich) return "";
  if (typeof rich === "string") return rich;
  const walk = (n) => (n.textData?.text ?? "") + (n.nodes ?? []).map(walk).join("");
  return (rich.nodes ?? []).map(walk).filter(Boolean).join("\n");
}

function toField(raw) {
  const io = raw.inputOptions ?? {};
  const block = io[INPUT_BLOCK[io.inputType]] ?? {};
  const compKey = Object.keys(block).find((k) => k !== "validation" && block[k] && typeof block[k] === "object" && "label" in block[k]);
  const comp = compKey ? block[compKey] : {};
  const type = block.componentType;
  const control =
    type === "PHONE_INPUT" ? "phone" :
    type === "DROPDOWN" ? "select" :
    type === "RADIO_GROUP" ? "radio" :
    type === "CHECKBOX_GROUP" ? "checkboxGroup" :
    type === "TEXT_INPUT" && raw.identifier === "TEXT_AREA" ? "textarea" :
    type === "TEXT_INPUT" && block.validation?.format === "EMAIL" ? "email" :
    type === "TEXT_INPUT" ? "text" : "unknown";
  return {
    id: raw.id,
    target: io.target,
    inputType: io.inputType,
    control,
    label: richToText(comp.label) || io.target,
    showLabel: comp.showLabel !== false,
    required: Boolean(io.required),
    hidden: Boolean(raw.hidden),
    placeholder: comp.placeholder || "",
    choices: (comp.options ?? []).map((o) => ({ value: o.value, label: o.label ?? o.value })),
    country: comp.defaultCountryCode || "",
  };
}

function toForm(raw) {
  const byId = new Map((raw.formFields ?? []).map((f) => [f.id, f]));
  const items = raw.steps?.[0]?.layout?.large?.items ?? [];
  const ordered = items.length
    ? [...items].sort((a, b) => a.row - b.row || a.column - b.column).map((i) => byId.get(i.fieldId)).filter(Boolean)
    : raw.formFields ?? [];
  const fields = ordered.filter((f) => f.fieldType === "INPUT" && !f.hidden).map(toField);
  const nav = (raw.formFields ?? []).find((f) => f.displayOptions?.pageNavigationOptions)?.displayOptions.pageNavigationOptions ?? {};
  const success = raw.submitSettings ?? {};
  return {
    id: raw.id ?? raw._id,
    fields,
    submitText: nav.submitText || "Envoyer",
    enabled: raw.enabled !== false,
    disabledMessage: richToText(raw.disabledFormMessage) || "",
    thankYou: success.submitSuccessAction === "THANK_YOU_MESSAGE" ? richToText(success.thankYouMessageOptions?.richContent) : "",
    redirectUrl: success.submitSuccessAction === "REDIRECT" ? success.redirectOptions?.redirectUrl : "",
  };
}

// ---- valeurs et validation ------------------------------------------------------------------

function normalizePhone(value, country) {
  let v = String(value ?? "").replace(/[^0-9+]/g, "");
  if (v.startsWith("00")) v = `+${v.slice(2)}`;
  if (!v.startsWith("+") && v.startsWith("0") && DIAL_CODES[country]) v = `+${DIAL_CODES[country]}${v.slice(1)}`;
  return v;
}

function readValue(root, field) {
  if (field.control === "checkboxGroup") {
    return [...root.querySelectorAll(`input[name="${field.target}"]:checked`)].map((i) => i.value);
  }
  if (field.control === "radio") {
    return root.querySelector(`input[name="${field.target}"]:checked`)?.value ?? "";
  }
  const el = root.querySelector(`[name="${field.target}"]`);
  return el ? el.value.trim() : "";
}

function validateField(field, value) {
  const empty = Array.isArray(value) ? value.length === 0 : value === "";
  if (field.required && empty) {
    if (["select", "radio", "checkboxGroup"].includes(field.control)) return "Choisissez une option.";
    if (field.control === "email") return "Indiquez une adresse e-mail.";
    if (field.control === "phone") return "Indiquez un numéro de téléphone.";
    return "Ce champ est obligatoire.";
  }
  if (empty) return "";
  if (field.control === "email" && !EMAIL_PATTERN.test(value)) return "Indiquez une adresse e-mail valide, par exemple nom@etablissement.re.";
  if (field.control === "phone" && !PHONE_PATTERN.test(normalizePhone(value, field.country))) return "Indiquez un numéro valide, par exemple 0692 12 34 56.";
  return "";
}

function toSubmissionValues(fields, root) {
  const out = {};
  for (const f of fields) {
    if (f.control === "unknown") continue;
    const v = readValue(root, f);
    if (Array.isArray(v)) {
      if (v.length) out[f.target] = v;
    } else if (v !== "") {
      out[f.target] = f.control === "phone" ? normalizePhone(v, f.country) : v;
    }
  }
  return out;
}

function serverErrors(err, fields) {
  const targets = new Set(fields.map((f) => f.target));
  const violations = err?.details?.validationError?.fieldViolations ?? [];
  const out = {};
  for (const v of violations.flatMap((x) => x.data?.errors ?? [x])) {
    const path = v?.errorPath;
    if (path && targets.has(path.split("/")[0])) {
      out[path.split("/")[0]] = v.useCustomErrorMessage && v.errorMessage ? v.errorMessage : "Vérifiez cette réponse.";
    }
  }
  return out;
}

// ---- rendu ----------------------------------------------------------------------------------

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const req = (f) => (f.required ? '<span class="req" aria-hidden="true">*</span>' : "");

function fieldHtml(f) {
  const id = `f-${f.target}`;
  const err = `<p class="err" id="err-${f.target}"></p>`;
  const labelAttr = f.showLabel ? "" : ` aria-label="${esc(f.label)}"`;
  const common = `name="${f.target}" id="${id}" aria-describedby="err-${f.target}"${f.required ? " required" : ""}${labelAttr}`;
  const label = f.showLabel ? `<label for="${id}">${esc(f.label)}${req(f)}</label>` : "";
  const ph = f.placeholder ? ` placeholder="${esc(f.placeholder)}"` : "";
  switch (f.control) {
    case "text":
    case "email":
    case "phone": {
      const type = f.control === "email" ? "email" : f.control === "phone" ? "tel" : "text";
      const auto = f.control === "email" ? ' autocomplete="email"' : f.control === "phone" ? ' autocomplete="tel"' : "";
      return `<div class="field">${label}<input type="${type}" ${common}${ph}${auto}>${err}</div>`;
    }
    case "textarea":
      return `<div class="field">${label}<textarea ${common}${ph}></textarea>${err}</div>`;
    case "select":
      return `<div class="field">${label}<select ${common}><option value="">Choisissez…</option>${f.choices
        .map((c) => `<option value="${esc(c.value)}">${esc(c.label)}</option>`).join("")}</select>${err}</div>`;
    case "radio":
    case "checkboxGroup": {
      const type = f.control === "radio" ? "radio" : "checkbox";
      return `<fieldset class="field" aria-describedby="err-${f.target}"><legend>${esc(f.label)}${req(f)}</legend>${f.choices
        .map((c, i) => `<label class="choice"><input type="${type}" name="${f.target}" value="${esc(c.value)}" id="${id}-${i}"> ${esc(c.label)}</label>`)
        .join("")}${err}</fieldset>`;
    }
    default:
      return `<div class="field"><p>${esc(f.label)} : ce champ n'est pas disponible ici, précisez-le dans votre message.</p></div>`;
  }
}

function setError(root, target, message) {
  const p = root.querySelector(`#err-${CSS.escape(target)}`);
  if (p) p.textContent = message || "";
  root.querySelectorAll(`[name="${target}"]`).forEach((el) => {
    if (message) el.setAttribute("aria-invalid", "true");
    else el.removeAttribute("aria-invalid");
  });
}

function showThanks(host, form) {
  const text = form.thankYou || "Merci ! Votre demande a bien été envoyée.";
  host.innerHTML = `<div class="thanks" tabindex="-1"><h3>Demande envoyée</h3>${text
    .split("\n").filter(Boolean).map((p) => `<p>${esc(p)}</p>`).join("")}</div>`;
  host.querySelector(".thanks").focus();
}

async function mount(host) {
  const formId = host.dataset.formId;
  let form;
  try {
    const res = await wixRequest(`/form-schema-service/v4/forms/${encodeURIComponent(formId)}`, { method: "GET" });
    if (!res?.form) throw new Error("form not found");
    form = toForm(res.form);
  } catch {
    host.innerHTML = '<p class="form-error">Le formulaire ne peut pas être chargé pour le moment. Écrivez-nous à <a href="mailto:contact.sirose@gmail.com">contact.sirose@gmail.com</a>.</p>';
    return;
  }
  if (!form.enabled) {
    host.innerHTML = `<p>${esc(form.disabledMessage || "Ce formulaire n'accepte plus de demandes pour le moment.")}</p>`;
    return;
  }

  host.innerHTML = `<form novalidate>
    <p class="form-error" hidden></p>
    ${form.fields.map(fieldHtml).join("")}
    <button type="submit" class="btn btn-primary">${esc(form.submitText)}</button>
  </form>`;
  const el = host.querySelector("form");
  const formError = el.querySelector(".form-error");
  const button = el.querySelector("button[type=submit]");
  const touched = new Set();

  el.addEventListener("focusout", (e) => {
    const target = e.target?.name;
    const field = form.fields.find((f) => f.target === target);
    if (!field) return;
    touched.add(target);
    setError(el, target, validateField(field, readValue(el, field)));
  });
  el.addEventListener("change", (e) => {
    const target = e.target?.name;
    const field = form.fields.find((f) => f.target === target);
    if (field && touched.has(target)) setError(el, target, validateField(field, readValue(el, field)));
  });

  el.addEventListener("submit", async (e) => {
    e.preventDefault();
    formError.hidden = true;
    let firstInvalid = null;
    for (const f of form.fields) {
      touched.add(f.target);
      const msg = validateField(f, readValue(el, f));
      setError(el, f.target, msg);
      if (msg && !firstInvalid) firstInvalid = el.querySelector(`[name="${f.target}"]`);
    }
    if (firstInvalid) {
      firstInvalid.focus();
      return;
    }
    button.disabled = true;
    try {
      const created = await wixRequest("/form-submission-service/v4/submissions", {
        body: { submission: { formId: form.id, submissions: toSubmissionValues(form.fields, el) } },
      });
      const status = created?.submission?.status;
      if (!SUBMITTED_OK.has(status)) throw new Error(`statut ${status}`);
      if (form.redirectUrl) {
        window.location.assign(form.redirectUrl);
        return;
      }
      showThanks(host, form);
    } catch (err) {
      const errs = serverErrors(err, form.fields);
      for (const [target, msg] of Object.entries(errs)) setError(el, target, msg);
      formError.textContent = Object.keys(errs).length
        ? "Certaines réponses sont à vérifier."
        : "L'envoi n'a pas abouti. Réessayez dans un instant ou écrivez-nous à contact.sirose@gmail.com.";
      formError.hidden = false;
      button.disabled = false;
    }
  });
}

const host = document.getElementById("wix-form");
if (host) mount(host);
