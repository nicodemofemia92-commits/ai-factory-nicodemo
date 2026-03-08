#!/bin/zsh
export PATH="/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"

if [ -f "$HOME/.zshrc" ]; then
  source "$HOME/.zshrc"
fi

cd "/Users/nicodemofemia/ai_factory"

echo "===== ROUTINE START $(date) =====" >> "/Users/nicodemofemia/ai_factory/logs/routine.out.log"

python3 "/Users/nicodemofemia/ai_factory/daily_pack.py" >> "/Users/nicodemofemia/ai_factory/logs/routine.out.log" 2>> "/Users/nicodemofemia/ai_factory/logs/routine.err.log"
python3 "/Users/nicodemofemia/ai_factory/client_hunter.py" >> "/Users/nicodemofemia/ai_factory/logs/routine.out.log" 2>> "/Users/nicodemofemia/ai_factory/logs/routine.err.log"
python3 "/Users/nicodemofemia/ai_factory/build_dashboard.py" >> "/Users/nicodemofemia/ai_factory/logs/routine.out.log" 2>> "/Users/nicodemofemia/ai_factory/logs/routine.err.log"

echo "===== ROUTINE END $(date) =====" >> "/Users/nicodemofemia/ai_factory/logs/routine.out.log"
