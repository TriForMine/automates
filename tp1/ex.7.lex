mot_clefs (False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonLocal|not|or|pass|raise|return|try|while|with|yield)
operateurs (\+|\-|\*|\*\*|\/\/|%|@|<<|>>|&|\||\^|~|<|>|<=|>=|==|!=|:=)
delimiteurs (\(|\)|\[|\]|\{|\}|\,|\:|\.|\;|\@|=|->|\+=|\-=|\*=|\/=|\/\/=|\%=|@=|&=|\|=|\^=|>>=|<<=|\*\*=)
identificateur ([a-zA-Z_][a-zA-Z0-9_]*)
chaine ((\"|\')([^\\\n|\'|\"]|(\\.))*?(\"|\'))
nombre_flottants (([0-9]+)\.([0-9]+))|(([0-9]+)\.([0-9]+)(e|E)(\+|\-)?([0-9]+))|(([0-9]+)(e|E)(\+|\-)?([0-9]+))
nombre_entiers (0b[0-1]+)|(0o[0-7]+)|(0x[0-9a-fA-F]+)|([0-9]+)
nombre_imaginaires ({nombre_flottants}|{nombre_entiers})(j|J)
commentaire (#.*)

%%
{mot_clefs} printf("Mot Clef: %s\n", yytext);
{operateurs} printf("Opérateur: %s\n", yytext);
{delimiteurs} printf("Délimiteur: %s\n", yytext);
{identificateur} printf("Identificateur: %s\n", yytext);
{chaine} printf("Chaine: %s\n", yytext);
{nombre_imaginaires} printf("Nombre Imaginaire: %s\n", yytext);
{nombre_flottants} printf("Nombre Flottants: %s\n", yytext);
{nombre_entiers} printf("Nombre Entier: %s\n", yytext);
{commentaire} printf("Commentaire: %s\n", yytext);
\n ;
. ;
%%
int main (int argc, char *argv[]) {
    yylex();
    return 0;
}
