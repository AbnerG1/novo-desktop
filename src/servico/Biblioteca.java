package servico;

import modelo.*;
import java.time.LocalDate;
import java.util.*;

public class Biblioteca {
    private final List<Item> itens = new ArrayList<>();             // ASSOCIAÇÃO (itens existem fora)
    private final List<Pessoa> pessoas = new ArrayList<>();         // ASSOCIAÇÃO
    private final List<Emprestimo> emprestimos = new ArrayList<>(); // COMPOSIÇÃO (criados aqui)

    public void adicionar(Item item) { itens.add(item); }
    public void adicionar(Pessoa pessoa) { pessoas.add(pessoa); }

    public List<Item> getItens() { return Collections.unmodifiableList(itens); }
    public List<Pessoa> getPessoas() { return Collections.unmodifiableList(pessoas); }

    public List<Emprestimo> ativos() {
        List<Emprestimo> r = new ArrayList<>();
        for (Emprestimo e : emprestimos) if (e.isAtivo()) r.add(e);
        return r;
    }

    public int ativosDe(Pessoa p) {
        int n = 0;
        for (Emprestimo e : ativos()) if (e.getPessoa() == p) n++;
        return n;
    }

    /** DEPENDÊNCIA de BibliotecaException (lança). */
    public Emprestimo emprestar(Pessoa p, Item i, LocalDate data) throws BibliotecaException {
        if (p == null || i == null) throw new BibliotecaException("Selecione pessoa e item.");
        if (!i.isDisponivel()) throw new BibliotecaException("Item já emprestado.");
        if (ativosDe(p) >= p.limiteEmprestimos())
            throw new BibliotecaException("Limite de " + p.limiteEmprestimos() + " empréstimos atingido.");
        Emprestimo e = new Emprestimo(p, i, data);
        emprestimos.add(e);
        return e;
    }

    public double devolver(Emprestimo e, LocalDate hoje) throws BibliotecaException {
        if (e == null || !e.isAtivo()) throw new BibliotecaException("Selecione um empréstimo ativo.");
        return e.devolver(hoje);
    }
}
