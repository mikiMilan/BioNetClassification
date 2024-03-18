import java.util.ArrayList;
import java.io.*;

public class srediTezinskuMrezu{
	
		
public static void main(String[]args){
	System.out.println("Ucitavanje u array list i mapiranje....");
	
	
	ArrayList <String> tezinskaMreza  = new ArrayList<String>();
	ArrayList <String> dupliraneGrane = new ArrayList<String>();
	
	
	try{
			BufferedReader br = new BufferedReader(new FileReader("biogridReduced_weight.txt"));
			String line;
			boolean eof = false;
			while(!eof){
				line = br.readLine();
				if(line==null)
					eof = true;
				else{
					tezinskaMreza.add(line);
				}
				
			}
			
			br.close();
		}
		catch(IOException e){
			System.out.println(e.toString());

		}
		
		System.out.println("Procitana biogrid tezinska mreza: "+tezinskaMreza.size());
		
		
		try{
			BufferedReader br = new BufferedReader(new FileReader("duplicated_rows.txt"));
			String line;
			boolean eof = false;
			while(!eof){
				line = br.readLine();
				if(line==null)
					eof = true;
				else{
					String [] niz = line.split("\t");
					String grana = niz[0]+"\t"+niz[1]+"\t"+niz[2];			
					dupliraneGrane.add(grana);
				}
				
			}
			
			br.close();
		}
		catch(IOException e){
			System.out.println(e.toString());

		}
		
		System.out.println("Procitane duplirane grane: "+dupliraneGrane.size());
		
				
			ArrayList <String> mrezaTezinskaFinal  = new ArrayList<String>();
			
		for(int i = 0; i< tezinskaMreza.size();i++){
			
			if(!dupliraneGrane.contains(tezinskaMreza.get(i)))
				mrezaTezinskaFinal.add(tezinskaMreza.get(i));
				
		   else{
		   	
		   	System.out.println("Duplirana grana: "+tezinskaMreza.get(i));
		   	
		   	
		   		String [] temp = tezinskaMreza.get(i).split("\t");
		   		String p = temp[0];
		   		String d = temp[1];
		   		String t1 = temp[2];
		   		String t2 = "";
		   		
		   		System.out.println("Procitano: "+p+" "+d+" "+t1);
		   		
		   		
		   		for(int j=0;j<dupliraneGrane.size();j++){
		   			String [] test = dupliraneGrane.get(j).split("\t");
		   			
		   			System.out.println("Procitano: "+test[0]+" "+test[1]+" "+test[2]);
		   			
		   			if(p.compareTo(test[1]) == 0 && d.compareTo(test[0])==0 && t1. compareTo(test[2])!=0)
		   				t2 = test[2];
		   		}
		   		
		   		double tezina = (Double.parseDouble(t1)+Double.parseDouble(t2))/2;
		   		
		   		if(!mrezaTezinskaFinal.contains(p+"\t"+d+"\t"+tezina) && !mrezaTezinskaFinal.contains(d+"\t"+p+"\t"+tezina))
		   			mrezaTezinskaFinal.add(p+"\t"+d+"\t"+tezina);
		   			System.out.println("Upisano: "+p+"\t"+d+"\t"+tezina);
		   	} 
			  
			
	}
		
		try{
			BufferedWriter bw = new BufferedWriter(new FileWriter("biogridWeihgt_Final.txt"));
			
			for(int a=0;a<mrezaTezinskaFinal.size();a++){
			bw.write(mrezaTezinskaFinal.get(a));
			bw.newLine();
	}

			bw.close();


	}catch(IOException e){
		System.out.println(e.toString());
	}
	
	

}
}