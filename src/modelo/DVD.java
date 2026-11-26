package modelo;

public class DVD extends Item {
    private final int duracaoMin;
    public DVD(String titulo, int duracaoMin) { super(titulo); this.duracaoMin = duracaoMin; }
    @Override public int prazoDias() { return 3; }
    @Override public double multaPorDia() { return 2.00; }
    @Override public String tipo() { return "DVD"; }
    @Override protected String detalhe() { return duracaoMin + " min"; }
}
