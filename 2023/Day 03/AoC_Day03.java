import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class AoC_Day03 {

   record NumberElement(int start, int end, int value){}

   record SymbolElement(int position, char value){
      public boolean isGear() {
         return value == '*';
      }
   }

   record Line(List<NumberElement> numbers,List<SymbolElement> symbols){
      public static Line empty = new Line(List.of(), List.of());
   }

   static class Window {
      private Line previousLine = Line.empty;
      private Line currentLine = Line.empty;
      private Line nextLine = Line.empty;

      public Window push(Line newLine) {
         previousLine = currentLine;
         currentLine = nextLine;
         nextLine = newLine;
         return this;
      }

      private Stream<Line> lines() {
         return Stream.of(previousLine, currentLine, nextLine);
      }

      public int calculatePartNumberValue() {
         return currentLine
                  .numbers()
                  .stream()
                  .filter(this::hasAdjacentSymbol)
                  .mapToInt(NumberElement::value)
                  .sum();
      }

      private boolean hasAdjacentSymbol(NumberElement number) {
         return lines()
                  .map(Line::symbols)
                  .flatMap(List::stream)
                  .anyMatch(symbol -> isAdjacent(symbol, number));
      }

      private static boolean isAdjacent(SymbolElement symbol, NumberElement number) {
         return number.start() <= symbol.position() + 1
                  && number.end() >= symbol.position() - 1;
      }

      public int calculateGearRatioValue() {
         return currentLine
                  .symbols()
                  .stream()
                  .filter(SymbolElement::isGear)
                  .mapToInt(this::calculateGearRatioValue)
                  .sum();
      }

      private int calculateGearRatioValue(SymbolElement symbol) {
         final Set<NumberElement> adjacentNumbers = lines()
                  .map(Line::numbers)
                  .flatMap(List::stream)
                  .filter(number -> isAdjacent(symbol, number))
                  .collect(Collectors.toSet());
         
         if (adjacentNumbers.size() == 2) {
            return adjacentNumbers.stream()
                     .mapToInt(NumberElement::value)
                     .reduce(1, (a, b) -> a * b);
         }
         
         return 0;
      }
   }

   public static void main(String[] args) throws IOException {
      try (Stream<String> lines = Files.lines(Path.of("AoC_Day03.input.txt"))) {
         var linesStream = lines.map(AoC_Day03::parse);
         Window window = new Window();
         int value = Stream.concat(linesStream, Stream.of(new Line(List.of(), List.of())))
                     .map(window::push)
                     .mapToInt(Window::calculatePartNumberValue)
                     .sum();
         System.out.println(value);
      }

      try (Stream<String> lines = Files.lines(Path.of("AoC_Day03.input.txt"))) {
         var linesStream = lines.map(AoC_Day03::parse);
         Window window = new Window();
         int value = Stream.concat(linesStream, Stream.of(Line.empty))
                     .map(window::push)
                     .mapToInt(Window::calculateGearRatioValue)
                     .sum();
         System.out.println(value);
      }
   }

   private static Line parse(String line) {
      List<NumberElement> numbers = new ArrayList<>();
      List<SymbolElement> symbols = new ArrayList<>();
      char[] chars = line.toCharArray();
      int current_number = 0;
      int current_digits = 0;
      
      for (int i = 0; i < line.length(); ++i) {
         char c = chars[i];
         if (Character.isDigit(c)) {
            ++current_digits;
            int digit = Character.digit(c, 10);
            current_number = current_number * 10 + digit;
         } else if (c == '.') {
            if (current_number > 0) {
               NumberElement number = new NumberElement(i-current_digits, i-1, current_number);
               numbers.add(number);
               current_number = 0;
               current_digits = 0;
            }
         } else {
            if (current_number > 0) {
               NumberElement number = new NumberElement(i-current_digits, i-1, current_number);
               numbers.add(number);
               current_number = 0;
               current_digits = 0;
            }
            
            SymbolElement symbol = new SymbolElement(i, c);
            symbols.add(symbol);
         }
      }
      
      if (current_number > 0) {
         NumberElement number = new NumberElement(chars.length - current_digits, chars.length - 1, current_number);
         numbers.add(number);
      }
      
      return new Line(numbers, symbols);
   }
}
