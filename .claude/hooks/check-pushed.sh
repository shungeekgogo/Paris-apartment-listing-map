#!/usr/bin/env bash
# Stop hook: 作業を終える前に、変更が GitHub に push 済みかを確認する。
# 未コミット・未 push があれば Claude に一度だけ差し戻す（別の PC で古いファイルにならないように）。

input=$(cat)
# 差し戻し後の2回目の停止では何もしない（無限ループ防止）
echo "$input" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true' && exit 0

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}" || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

upstream=$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null) || exit 0
[ -n "$upstream" ] || exit 0

dirty=$(git status --porcelain)
ahead=$(git rev-list --count "$upstream..HEAD" 2>/dev/null || echo 0)

if [ -n "$dirty" ] || [ "$ahead" -gt 0 ]; then
  echo "GitHub に未反映の変更があります（未コミット: $(printf '%s' "$dirty" | grep -c .) ファイル / 未 push コミット: ${ahead} 件）。コミットして git push（$upstream）してから終了してください。" >&2
  exit 2
fi
exit 0
