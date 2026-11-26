package modelo;

/** Classe abstrata: base da HERANÇA de itens do acervo. */
public abstract class Item {
    private static int sequencia = 1;
    private final int id = sequencia++;
    private final String titulo;
    private boolean disponivel = true;

    protected Item(String titulo) { this.titulo = titulo; }

    public int getId() { return id; }
    public String getTitulo() { return titulo; }
    public boolean isDisponivel() { return disponivel; }
    public void setDisponivel(boolean disponivel) { this.disponivel = disponivel; }

    // POLIMORFISMO: cada subclasse define sua regra
    public abstract int prazoDias();
    public abstract double multaPorDia();
    public abstract String tipo();
    protected abstract String detalhe();

    @Override public String toString() {
        return tipo() + " #" + id + " - " + titulo + " (" + detalhe() + ")"
             + (disponivel ? "" : " [EMPRESTADO]");
    }
}
