#!/bin/bash
# Compila e gera a versão gráfica do diagrama de trasições
fstcompile --isymbols=transicoes.sym --osymbols=transicoes.sym  diagrama.txt | fstarcsort > diagrama.fst
fstdraw    --isymbols=transicoes.sym --osymbols=transicoes.sym  diagrama.fst | dot -Tpdf  > diagrama.pdf
