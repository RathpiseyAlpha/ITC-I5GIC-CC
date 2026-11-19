"""Point the PDF's Vite client at the local Lab 5 FastAPI service."""

import argparse
from pathlib import Path


def replace_once(text, before, after):
    if after in text:
        return text
    if text.count(before) != 1:
        raise ValueError(f"Unexpected starter file. Could not locate {before!r}.")
    return text.replace(before, after, 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path, help="Path to the DatabaseOptions checkout")
    args = parser.parse_args()
    client = args.checkout / "socialmedia"
    axios = client / "src/Pages/axiosConfig.js"
    vite = client / "vite.config.js"
    posts = client / "src/Pages/MainPage/index.jsx"

    changes = {
        axios: replace_once(
            axios.read_text(encoding="utf-8"),
            "baseURL: 'http://<Your_Instance_PublicIP>:8000'",
            "baseURL: '/api'",
        ),
        vite: replace_once(
            vite.read_text(encoding="utf-8"),
            "  plugins: [react()],",
            "  plugins: [react()],\n"
            "  server: {\n"
            "    proxy: {\n"
            "      '/api': {\n"
            "        target: 'http://127.0.0.1:8000',\n"
            "        rewrite: (path) => path.slice(4),\n"
            "      },\n"
            "    },\n"
            "  },",
        ),
        posts: replace_once(
            posts.read_text(encoding="utf-8"),
            "  const onlogout = (e) => {\n    e.preventDefault();",
            "  const onlogout = async (e) => {\n    e.preventDefault();\n    await axios.post('/logout');",
        ),
    }
    # The upstream error branch calls a setter that is not defined on the post page.
    changes[posts] = replace_once(
        changes[posts],
        "  setLoading(false);\n  navigate('/');\n  console.log(error);",
        "  window.alert(error.response?.data?.detail || 'Could not publish the post.');",
    )
    for path, text in changes.items():
        path.write_text(text, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
