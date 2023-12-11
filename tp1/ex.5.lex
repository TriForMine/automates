    // déclarations en C
    int lignes = 0;
    int mots = 0;
    int caracteres = 0;
%%
. ++caracteres; REJECT;
([^\n|\ ](\ |\n)) ++mots; REJECT;
\n ++lignes; ++caracteres;
. ;
%%
int main (int argc, char *argv[]) {
    yylex();
    printf("Lignes: %d\nMots: %d\nCaractères: %d\n", lignes, mots, caracteres);
    return 0;
}
