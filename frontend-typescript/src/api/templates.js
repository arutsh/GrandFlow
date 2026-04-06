export async function fetchTemplates() {
    // return mock when backend unavailable:
    return (await fetch("/mock-templates.json").then((r) => r.json()));
}
