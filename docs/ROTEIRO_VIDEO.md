# Roteiro do vídeo (máx. 3:00)

Prepare antes de gravar: aba 1 = diagrama UML (README no GitHub ou plantuml.com), aba 2 = IDE com `Item.java`/`Livro.java`, app aberto (`java -cp out Main`), terminal pronto para `java -cp out TestesRunner`.

| Tempo | O que mostrar / falar |
|---|---|
| 0:00–0:15 | "Sou o Abner, projeto desktop de Orientação a Objetos: Biblioteca Universitária em Java Swing. Repositório público no GitHub." |
| 0:15–1:05 | **UML**: Herança (Item→Livro/Revista/DVD; Pessoa→Aluno/Professor) · Polimorfismo (prazoDias, multaPorDia, limiteEmprestimos) · Composição (Pessoa◆Endereco, Biblioteca◆Emprestimo) · Associação (Emprestimo→Pessoa/Item, Biblioteca→Item/Pessoa) · Dependência (Biblioteca⇢BibliotecaException, Emprestimo⇢LocalDate, Tela⇢Livro/Aluno) |
| 1:05–1:20 | **Código**: `Item` abstrata + `Livro` sobrescrevendo `prazoDias()`/`multaPorDia()`; `Pessoa` criando `new Endereco(...)` |
| 1:20–2:40 | **Demo (testar todas as funcionalidades)** — ver checklist abaixo |
| 2:40–3:00 | Terminal: `java -cp out TestesRunner` → "18 OK, 0 falhas". Encerrar. |

## Checklist da demo
1. **Acervo**: adicionar Livro (`POO` / `Gamma`), Revista (`Veja` / `2800`), DVD (`Interestelar` / `169`). Erro: edição `abc` → aviso.
2. **Pessoas**: adicionar Aluno e Professor. Erro: campo vazio → aviso.
3. **Emprestar** Aluno + Livro → aparece em empréstimos; item fica `[EMPRESTADO]`.
4. **Erro**: emprestar o mesmo livro de novo → "Item já emprestado."
5. **Devolver** Livro com **20** dias → multa **R$ 6,00** (polimorfismo).
6. **Emprestar + devolver** DVD com **5** dias → multa **R$ 4,00**.
7. (Se sobrar tempo) 4º empréstimo do Aluno → "Limite de 3..."; Professor consegue.

## Entrega
1. Repositório **público**: GitHub → Settings → General → Danger Zone → Change visibility → Public.
2. Gravar a tela (Windows: Win+G · Android: gravador de tela · ou OBS), subir no YouTube (Público ou Não listado).
3. Na plataforma Metabloom, colar: link do repositório + link do vídeo.
