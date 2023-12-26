package org.example;

import com.sun.source.util.JavacTask;
import com.sun.source.tree.CompilationUnitTree;
import com.sun.source.tree.ClassTree;
import com.sun.source.tree.MethodTree;
import com.sun.source.tree.Tree;

import java.io.File;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import javax.tools.JavaCompiler;
import javax.tools.JavaFileObject;
import javax.tools.StandardJavaFileManager;
import javax.tools.ToolProvider;

public class Main {

    public static void main(final String[] args) throws Exception {
        final JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
        try (final StandardJavaFileManager fileManager = compiler.getStandardFileManager(null, null, StandardCharsets.UTF_8)) {
            final Iterable<? extends JavaFileObject> compilationUnits = fileManager.getJavaFileObjectsFromFiles(List.of(new File(args[0])));
            final JavacTask javacTask = (JavacTask) compiler.getTask(null, fileManager, null, null, null, compilationUnits);
            final Iterable<? extends CompilationUnitTree> compilationUnitTrees = javacTask.parse();
            final ClassTree classTree = (ClassTree) compilationUnitTrees.iterator().next().getTypeDecls().get(0);
            final List<? extends Tree> classMemberList = classTree.getMembers();
            final List<MethodTree> classMethodMemberList = classMemberList.stream()
                    .filter(MethodTree.class::isInstance)
                    .map(MethodTree.class::cast)
                    .collect(Collectors.toList());
            // just prints the names of the methods
            for (var i :
                    classMethodMemberList) {
                String params = "";
                for (int j=0; j< i.getParameters().size(); ++j){
                    params += i.getParameters().get(j);
                    if (j != i.getParameters().size()-1){
                        params += ", ";
                    }
                }
                
                System.out.println(classTree.getSimpleName() + ":+:+:" + i.getName().toString() + "(" + params + ")" + ":+:+:" + i.getReturnType());
            }
        }
    }

}