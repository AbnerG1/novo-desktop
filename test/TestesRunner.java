import modelo.*;
import servico.*;
import java.time.LocalDate;

/** Testes sem dependências externas. Rodar: java -cp out TestesRunner */
public class TestesRunner {
    static int ok = 0, falhas = 0;
    interface Acao { void executar() throws Exception; }

    static void check(String nome, boolean cond) {
        if (cond) ok++; else falhas++;
        System.out.println((cond ? "[OK]    " : "[FALHA] ") + nome);
    }
    static void lanca(String nome, Acao a) {
        try { a.executar(); check(nome, false); }
        catch (BibliotecaException e) { check(nome + " -> \"" + e.getMessage() + "\"", true); }
        catch (Exception e) { check(nome, false); }
    }

    public static void main(String[] args) throws Exception {
        LocalDate hoje = LocalDate.of(2026, 11, 25);
        Item livro = new Livro("Clean Code", "Robert Martin");
        Item revista = new Revista("Super", 450);
        Item dvd = new DVD("Matrix", 136);
        Pessoa aluno = new Aluno("Abner", "240000001", "Rua 1", "Brasília");
        Pessoa prof = new Professor("Ana", "FCTE", "Rua 2", "Gama");

        // Herança + polimorfismo
        check("Prazos polimórficos 14/7/3", livro.prazoDias() == 14 && revista.prazoDias() == 7 && dvd.prazoDias() == 3);
        check("Multas polimórficas 1.0/0.5/2.0", livro.multaPorDia() == 1.0 && revista.multaPorDia() == 0.5 && dvd.multaPorDia() == 2.0);
        check("Limites polimórficos 3/5", aluno.limiteEmprestimos() == 3 && prof.limiteEmprestimos() == 5);
        check("Item é Item (herança)", livro instanceof Item && aluno instanceof Pessoa);
        // Composição
        check("Pessoa compõe Endereço", aluno.getEndereco().toString().equals("Rua 1, Brasília"));

        Biblioteca b = new Biblioteca();
        b.adicionar(livro); b.adicionar(revista); b.adicionar(dvd); b.adicionar(aluno); b.adicionar(prof);
        check("Cadastro de itens e pessoas", b.getItens().size() == 3 && b.getPessoas().size() == 2);

        // Empréstimo
        Emprestimo e1 = b.emprestar(aluno, livro, hoje);
        check("Empréstimo marca item indisponível", !livro.isDisponivel() && b.ativos().size() == 1);
        check("Vencimento = data + prazo do livro", e1.vencimento().equals(hoje.plusDays(14)));
        lanca("Emprestar item já emprestado", () -> b.emprestar(prof, livro, hoje));
        lanca("Emprestar sem seleção", () -> b.emprestar(null, null, hoje));

        // Devolução e multas
        check("Devolução no prazo = R$ 0", b.devolver(e1, hoje.plusDays(14)) == 0.0);
        check("Devolução libera o item", livro.isDisponivel() && b.ativos().isEmpty());
        lanca("Devolver empréstimo já devolvido", () -> b.devolver(e1, hoje));
        check("Multa Livro 6 dias atraso = 6.00", b.devolver(b.emprestar(aluno, livro, hoje), hoje.plusDays(20)) == 6.0);
        check("Multa Revista 3 dias atraso = 1.50", b.devolver(b.emprestar(aluno, revista, hoje), hoje.plusDays(10)) == 1.5);
        check("Multa DVD 2 dias atraso = 4.00", b.devolver(b.emprestar(aluno, dvd, hoje), hoje.plusDays(5)) == 4.0);

        // Limite
        Biblioteca b2 = new Biblioteca();
        for (int i = 0; i < 4; i++) b2.adicionar(new Livro("L" + i, "A"));
        for (int i = 0; i < 3; i++) b2.emprestar(aluno, b2.getItens().get(i), hoje);
        lanca("Aluno acima do limite (3)", () -> b2.emprestar(aluno, b2.getItens().get(3), hoje));
        check("Professor ainda pode (limite 5)", b2.emprestar(prof, b2.getItens().get(3), hoje) != null);

        System.out.println("\nResultado: " + ok + " OK, " + falhas + " falhas");
        System.exit(falhas == 0 ? 0 : 1);
    }
}
