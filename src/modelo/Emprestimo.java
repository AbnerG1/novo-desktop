package modelo;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

/** ASSOCIAÇÃO entre Pessoa e Item (conhece os dois). */
public class Emprestimo {
    private final Pessoa pessoa;
    private final Item item;
    private final LocalDate data;
    private boolean ativo = true;

    public Emprestimo(Pessoa pessoa, Item item, LocalDate data) {
        this.pessoa = pessoa; this.item = item; this.data = data;
        item.setDisponivel(false);
    }

    public Pessoa getPessoa() { return pessoa; }
    public Item getItem() { return item; }
    public LocalDate getData() { return data; }
    public boolean isAtivo() { return ativo; }
    public LocalDate vencimento() { return data.plusDays(item.prazoDias()); }

    /** DEPENDÊNCIA de LocalDate (parâmetro). Retorna a multa (polimórfica via Item). */
    public double devolver(LocalDate hoje) {
        ativo = false;
        item.setDisponivel(true);
        long atraso = Math.max(0, ChronoUnit.DAYS.between(vencimento(), hoje));
        return atraso * item.multaPorDia();
    }

    @Override public String toString() {
        return item.getTitulo() + " -> " + pessoa.getNome() + " (vence " + vencimento() + ")";
    }
}
