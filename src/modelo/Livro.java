package modelo;

public class Livro extends Item {
    private final String autor;
    public Livro(String titulo, String autor) { super(titulo); this.autor = autor; }
    @Override public int prazoDias() { return 14; }
    @Override public double multaPorDia() { return 1.00; }
    @Override public String tipo() { return "Livro"; }
    @Override protected String detalhe() { return "autor: " + autor; }
}
