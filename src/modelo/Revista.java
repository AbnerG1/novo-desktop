package modelo;

public class Revista extends Item {
    private final int edicao;
    public Revista(String titulo, int edicao) { super(titulo); this.edicao = edicao; }
    @Override public int prazoDias() { return 7; }
    @Override public double multaPorDia() { return 0.50; }
    @Override public String tipo() { return "Revista"; }
    @Override protected String detalhe() { return "edição " + edicao; }
}
